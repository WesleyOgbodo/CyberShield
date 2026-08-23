from flask import Blueprint, render_template, session
from models.security import recent_scans, recent_alerts, recent_activity, recent_logins
from utils.auth import login_required


dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
def index():
    uid = session['user_id']
    return render_template(
        'dashboard.html',
        scans=recent_scans(uid, 8),
        alerts=recent_alerts(uid, 8),
        activities=recent_activity(uid, 8),
        logins=recent_logins(uid, 8)
    )
