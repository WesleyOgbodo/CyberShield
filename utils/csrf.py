import hmac
import secrets
from flask import session, request


def get_csrf_token():
    token = session.get('_csrf_token')
    if not token:
        token = secrets.token_urlsafe(32)
        session['_csrf_token'] = token
    return token


def validate_csrf():
    submitted = request.form.get('_csrf_token', '')
    expected = session.get('_csrf_token', '')
    return bool(submitted and expected and hmac.compare_digest(submitted, expected))
