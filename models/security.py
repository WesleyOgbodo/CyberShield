from models.db import query_one, query_all, execute


def create_otp(user_id, otp_hash, expires_at):
    execute('UPDATE otp_codes SET used_at = NOW() WHERE user_id = %s AND used_at IS NULL', (user_id,))
    return execute(
        'INSERT INTO otp_codes (user_id, otp_hash, expires_at) VALUES (%s, %s, %s)',
        (user_id, otp_hash, expires_at)
    )


def get_latest_otp(user_id):
    return query_one(
        'SELECT * FROM otp_codes WHERE user_id = %s AND used_at IS NULL ORDER BY id DESC LIMIT 1',
        (user_id,)
    )


def mark_otp_used(otp_id):
    execute('UPDATE otp_codes SET used_at = NOW() WHERE id = %s', (otp_id,))


def log_login(user_id, username, success, ip_address, user_agent, reason=None):
    return execute(
        '''INSERT INTO login_logs (user_id, username_attempted, success, ip_address, user_agent, reason)
           VALUES (%s, %s, %s, %s, %s, %s)''',
        (user_id, username, success, ip_address, (user_agent or '')[:512], reason)
    )


def failed_attempts(username, ip_address, window_minutes=15):
    row = query_one(
        '''SELECT COUNT(*) AS count FROM login_logs
           WHERE success = 0 AND username_attempted = %s AND ip_address = %s
           AND created_at >= (NOW() - INTERVAL %s MINUTE)''',
        (username, ip_address, window_minutes)
    )
    return int(row['count']) if row else 0


def create_alert(user_id, alert_type, severity, title, message):
    return execute(
        '''INSERT INTO security_alerts (user_id, alert_type, severity, title, message)
           VALUES (%s, %s, %s, %s, %s)''',
        (user_id, alert_type, severity, title, message)
    )


def create_activity(user_id, action, details, ip_address=None):
    return execute(
        'INSERT INTO activity_logs (user_id, action, details, ip_address) VALUES (%s, %s, %s, %s)',
        (user_id, action, details, ip_address)
    )


def save_scan(user_id, url, result, score, triggered_rules):
    return execute(
        '''INSERT INTO phishing_scans (user_id, url, result, risk_score, triggered_rules)
           VALUES (%s, %s, %s, %s, %s)''',
        (user_id, url, result, score, triggered_rules)
    )


def recent_scans(user_id, limit=10):
    return query_all(
        'SELECT * FROM phishing_scans WHERE user_id = %s ORDER BY created_at DESC LIMIT %s',
        (user_id, limit)
    )


def recent_alerts(user_id, limit=10):
    return query_all(
        'SELECT * FROM security_alerts WHERE user_id = %s ORDER BY created_at DESC LIMIT %s',
        (user_id, limit)
    )


def recent_activity(user_id, limit=20):
    return query_all(
        'SELECT * FROM activity_logs WHERE user_id = %s ORDER BY created_at DESC LIMIT %s',
        (user_id, limit)
    )


def recent_logins(user_id, limit=20):
    return query_all(
        'SELECT * FROM login_logs WHERE user_id = %s ORDER BY created_at DESC LIMIT %s',
        (user_id, limit)
    )


def has_recent_intrusion_alert(user_id, window_minutes=15):
    row = query_one(
        '''SELECT id FROM security_alerts
           WHERE user_id = %s AND alert_type = 'intrusion'
           AND created_at >= (NOW() - INTERVAL %s MINUTE)
           ORDER BY id DESC LIMIT 1''',
        (user_id, window_minutes)
    )
    return bool(row)
