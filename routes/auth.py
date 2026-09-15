from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import create_user, get_by_username, get_by_email
from models.security import create_otp, get_latest_otp, mark_otp_used, log_login, failed_attempts, create_alert, create_activity, has_recent_intrusion_alert
from pymysql.err import MySQLError, IntegrityError
from utils.otp import generate_otp, hash_otp, expiry_time, verify_otp_hash
from utils.csrf import validate_csrf


auth_bp = Blueprint('auth', __name__)
MAX_FAILED_ATTEMPTS = 3


def client_ip():
    return request.remote_addr or 'unknown'


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form_data = {'username': '', 'email': ''}

    if request.method == 'POST':
        if not validate_csrf():
            flash('Invalid security token. Please refresh the page and try again.', 'danger')
            return render_template('register.html', form_data=form_data), 400

        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        form_data.update(username=username, email=email)

        if len(username) < 3 or len(username) > 50:
            flash('Username must be between 3 and 50 characters.', 'danger')
        elif '@' not in email or '.' not in email.split('@')[-1] or len(email) > 120:
            flash('Enter a valid email address.', 'danger')
        elif len(password) < 8:
            flash('Password must be at least 8 characters.', 'danger')
        elif password != confirm:
            flash('Passwords do not match.', 'danger')
        else:
            try:
                if get_by_username(username):
                    flash('Username already exists.', 'danger')
                elif get_by_email(email):
                    flash('Email address already exists.', 'danger')
                else:
                    create_user(username, email, generate_password_hash(password))
                    flash('Registration successful. You can now log in.', 'success')
                    return redirect(url_for('auth.login'))
            except IntegrityError as exc:
                current_app.logger.exception('Registration database integrity error: %s', exc)
                flash('That username or email is already registered. Please use different details.', 'danger')
            except MySQLError as exc:
                current_app.logger.exception('Registration database error: %s', exc)
                flash('Database error: could not save the account. Check that MySQL is running and that your .env settings match the database.', 'danger')
            except Exception as exc:
                current_app.logger.exception('Unexpected registration error: %s', exc)
                flash('Unexpected registration error. Check the VS Code terminal for details.', 'danger')

    return render_template('register.html', form_data=form_data)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not validate_csrf():
            flash('Invalid security token. Please try again.', 'danger')
            return render_template('login.html'), 400
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        ip = client_ip()

        try:
            user = get_by_username(username)
        except MySQLError:
            flash('Database connection failed. Make sure MySQL is running and your .env settings are correct.', 'danger')
            return render_template('login.html'), 503

        valid = bool(user and check_password_hash(user['password_hash'], password))
        if not valid:
            try:
                log_login(user['id'] if user else None, username, False, ip, request.user_agent.string, 'Invalid username or password')
                attempts = failed_attempts(username, ip)
                if user:
                    create_activity(user['id'], 'LOGIN_FAILED', f'Failed login attempt #{attempts}', ip)
                if attempts >= MAX_FAILED_ATTEMPTS:
                    if user and not has_recent_intrusion_alert(user['id']):
                        create_alert(user['id'], 'intrusion', 'high', 'Repeated failed login attempts',
                                     f'{attempts} failed login attempts were detected within the monitoring window.')
                    flash('Intrusion alert triggered after repeated failed login attempts.', 'danger')
                else:
                    flash('Invalid username or password.', 'danger')
            except MySQLError:
                flash('Database error while recording the login attempt. Check your MySQL connection.', 'danger')
            return render_template('login.html')

        try:
            log_login(user['id'], username, True, ip, request.user_agent.string, 'Password accepted')
            otp = generate_otp()
            create_otp(user['id'], hash_otp(otp), expiry_time())
        except MySQLError:
            flash('Database error while starting MFA. Check your MySQL connection.', 'danger')
            return render_template('login.html'), 503

        session.clear()
        session['pending_user_id'] = user['id']
        session['pending_username'] = user['username']
        session['demo_otp'] = otp
        flash('Password accepted. Enter the OTP to complete MFA.', 'info')
        return redirect(url_for('auth.verify_otp'))
    return render_template('login.html')


@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    user_id = session.get('pending_user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        if not validate_csrf():
            flash('Invalid security token. Please try again.', 'danger')
            return render_template('otp.html', demo_otp=session.get('demo_otp')), 400
        entered = request.form.get('otp', '').strip()
        try:
            record = get_latest_otp(user_id)
            if not record:
                flash('No active OTP was found. Please log in again.', 'danger')
                return redirect(url_for('auth.login'))
            if datetime.now(timezone.utc).replace(tzinfo=None) > record['expires_at']:
                flash('OTP has expired. Please log in again.', 'danger')
                return redirect(url_for('auth.login'))
            if not verify_otp_hash(entered, record['otp_hash']):
                flash('Invalid OTP.', 'danger')
                return render_template('otp.html', demo_otp=session.get('demo_otp'))
            mark_otp_used(record['id'])
            username = session.get('pending_username')
            session.clear()
            session.permanent = True
            session['user_id'] = user_id
            session['username'] = username
            session['mfa_verified'] = True
            create_activity(user_id, 'LOGIN_SUCCESS', 'Successful username/password and OTP authentication', client_ip())
            flash('Authentication successful. Welcome to your dashboard.', 'success')
            return redirect(url_for('dashboard.index'))
        except MySQLError:
            flash('Database error while verifying OTP. Check your MySQL connection.', 'danger')
            return render_template('otp.html', demo_otp=session.get('demo_otp')), 503

    return render_template('otp.html', demo_otp=session.get('demo_otp'))


@auth_bp.route('/logout', methods=['POST'])
def logout():
    if not validate_csrf():
        flash('Invalid security token. Please try again.', 'danger')
        return redirect(url_for('dashboard.index'))
    user_id = session.get('user_id')
    if user_id:
        try:
            create_activity(user_id, 'LOGOUT', 'User logged out securely', client_ip())
        except MySQLError:
            pass
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))
