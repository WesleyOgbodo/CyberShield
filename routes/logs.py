from flask import Blueprint, render_template, session
from models.security import recent_activity, recent_logins, recent_scans
from utils.auth import login_required

logs_bp = Blueprint('logs', __name__, url_prefix='/logs')


@logs_bp.route('/')
@login_required
def index():
    uid = session['user_id']
    return render_template('logs.html', activities=recent_activity(uid, 50), logins=recent_logins(uid, 50), scans=recent_scans(uid, 50))
