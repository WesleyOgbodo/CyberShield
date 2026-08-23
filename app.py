import os
from pathlib import Path
from flask import Flask, render_template
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

from models.db import close_db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.scanner import scanner_bp
from routes.logs import logs_bp
from routes.alerts import alerts_bp
from utils.csrf import get_csrf_token


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-this-in-production')
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', '0') == '1'
    app.config['PERMANENT_SESSION_LIFETIME'] = int(os.getenv('SESSION_LIFETIME', '1800'))

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(scanner_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(alerts_bp)

    @app.context_processor
    def inject_csrf_token():
        return {'csrf_token': get_csrf_token()}

    app.teardown_appcontext(close_db)

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/health')
    def health():
        return {'status': 'ok'}, 200

    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html', code=404, message='Page not found.'), 404

    @app.errorhandler(500)
    def server_error(error):
        app.logger.exception('Unhandled server error', exc_info=error)
        return render_template('error.html', code=500, message='An unexpected server error occurred.'), 500

    return app


app = create_app()

if __name__ == '__main__':
    # Development fallback. Normal Windows use should be through server.py/run_windows.bat.
    app.run(
        host=os.getenv('HOST', '127.0.0.1'),
        port=int(os.getenv('PORT', '5000')),
        debug=os.getenv('FLASK_DEBUG', '0') == '1',
        use_reloader=False,
    )
