from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get('user_id') or not session.get('mfa_verified'):
            flash('Please complete authentication before accessing this page.', 'warning')
            return redirect(url_for('auth.login'))
        session.permanent = True
        return view(*args, **kwargs)
    return wrapped
