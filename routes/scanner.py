from flask import Blueprint, render_template, request, session, flash
from models.security import save_scan, create_activity, create_alert
from utils.auth import login_required
from utils.phishing import analyze_url
from utils.csrf import validate_csrf


scanner_bp = Blueprint('scanner', __name__, url_prefix='/scanner')


@scanner_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    result = None
    url = ''
    if request.method == 'POST':
        if not validate_csrf():
            flash('Invalid security token. Please try again.', 'danger')
            return render_template('scanner.html', result=None, url=''), 400
        url = request.form.get('url', '').strip()
        if not url or len(url) > 2048:
            flash('Enter a valid URL (maximum 2048 characters).', 'danger')
        else:
            result = analyze_url(url)
            save_scan(session['user_id'], url, result['result'], result['score'], '; '.join(result['rules']) or 'No suspicious rules triggered')
            create_activity(session['user_id'], 'URL_SCAN', f"Scanned URL; result={result['result']}; score={result['score']}", request.remote_addr)
            if result['result'] == 'phishing':
                create_alert(session['user_id'], 'phishing', 'high', 'Potential phishing URL detected',
                             f'A scanned URL triggered {len(result["rules"])} suspicious rule(s).')
    return render_template('scanner.html', result=result, url=url)
