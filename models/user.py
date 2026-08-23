from models.db import query_one, execute


def create_user(username, email, password_hash):
    return execute(
        'INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)',
        (username, email, password_hash)
    )


def get_by_username(username):
    return query_one('SELECT * FROM users WHERE username = %s', (username,))


def get_by_id(user_id):
    return query_one('SELECT * FROM users WHERE id = %s', (user_id,))


def get_by_email(email):
    return query_one('SELECT * FROM users WHERE email = %s LIMIT 1', (email,))
