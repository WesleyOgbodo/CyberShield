import os
import pymysql
from flask import g
from pymysql.err import MySQLError


def get_db():
    if "db" not in g:
        g.db = pymysql.connect(
            host=os.getenv("DB_HOST", os.getenv("MYSQL_HOST", "localhost")),
            port=int(os.getenv("DB_PORT", os.getenv("MYSQL_PORT", "3306"))),
            user=os.getenv("DB_USER", os.getenv("MYSQL_USER", "root")),
            password=os.getenv("DB_PASSWORD", os.getenv("MYSQL_PASSWORD", "")),
            database=os.getenv("DB_NAME", os.getenv("MYSQL_DATABASE", "integrated_cybersecurity")),
            connect_timeout=10,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
        )
    return g.db


def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        try:
            db.close()
        except Exception:
            pass


def query_one(sql, params=()):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchone()


def query_all(sql, params=()):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchall()


def execute(sql, params=(), commit=True):
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, params)
            lastrowid = cursor.lastrowid
        if commit:
            db.commit()
        return lastrowid
    except MySQLError:
        if commit:
            db.rollback()
        raise
