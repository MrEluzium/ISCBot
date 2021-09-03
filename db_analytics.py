import sqlite3
from typing import Tuple

conn = sqlite3.connect('service.db', check_same_thread=False)
cursor = conn.cursor()


def get_return_user_id():
    cursor.execute("SELECT user_id FROM users")
    return cursor.fetchall()


def get_return_total_users():
    cursor.execute("SELECT id FROM users")
    return cursor.fetchall()


def get_return_total_homework():
    cursor.execute("SELECT id FROM homework")
    return cursor.fetchall()


def get_return_total_class():
    cursor.execute("SELECT id FROM schools")
    return cursor.fetchall()


def get_signup_class(values: Tuple):
    cursor.execute(f"INSERT INTO schools(school_name, class_name, token, editor_token) VALUES(?, ?, ?, ?);", values)
    conn.commit()
