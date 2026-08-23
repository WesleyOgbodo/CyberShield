from flask import Blueprint, render_template, session
from models.security import recent_alerts
from utils.auth import login_required

alerts_bp = Blueprint('alerts', __name__, url_prefix='/alerts')


@alerts_bp.route('/')
@login_required
def index():
    return render_template('alerts.html', alerts=recent_alerts(session['user_id'], 50))
