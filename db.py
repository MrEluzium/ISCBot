import sqlite3
from typing import Tuple

conn = sqlite3.connect('service.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY NOT NULL,
    username TEXT,
    school_id INTEGER REFERENCES schools(id) NOT NULL,
    role TEXT NOT NULL,
    user_id INTEGER NOT NULL);
""")
conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS schools(
    id INTEGER PRIMARY KEY NOT NULL,
    school_name TEXT NOT NULL,
    class_name TEXT NOT NULL,
    token TEXT NOT NULL,
    editor_token INTEGER NOT NULL);
""")
conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS homework(
    id INTEGER PRIMARY KEY NOT NULL,
    subject TEXT NOT NULL,
    title TEXT NOT NULL,
    created_at TIMESTAMP DATE DEFAULT (datetime('now','localtime')),
    user_id INTEGER NOT NULL,
    token TEXT NOT NULL);
""")
conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS roles(
    id INTEGER PRIMARY KEY NOT NULL,
    role TEXT NOT NULL);
""")


def get_check_user_profile():  # Проверка наличия пользователя в БД
    cursor.execute(f"SELECT user_id FROM users")
    return cursor.fetchall()


def get_check_class_token():  # Просмотр всех токенов для проверки входного токена
    cursor.execute(f"SELECT token FROM schools")
    return cursor.fetchall()


def get_check_user_role(user_id: int):  # Просмотор роли
    cursor.execute(f"SELECT role FROM users WHERE user_id={user_id}")
    return cursor.fetchall()


def get_add_user_profile(values: Tuple):  # Добавление нового пользователя
    cursor.execute(f"INSERT INTO users(username, school_id, role, user_id) VALUES(?, ?, ?, ?);", values)
    conn.commit()


def get_check_school_id(token: str):  # Достаем ID класса по токену
    cursor.execute(f"SELECT id FROM schools WHERE token='{token}'")
    return cursor.fetchall()


def get_return_school_id(user_id: int):  # Достаем school_id для дальнейшего возврата token
    cursor.execute(f"SELECT school_id FROM users WHERE user_id={user_id}")
    return cursor.fetchall()


def get_return_token(id: int):  # Возвращаем token по school_id
    cursor.execute(f"SELECT token FROM schools WHERE id={id}")
    return cursor.fetchall()


def get_add_homework(values: Tuple):
    cursor.execute(f"INSERT INTO homework(subject, title, user_id, token) VALUES(?, ?, ?, ?);", values)
    conn.commit()


def get_view_homework(token: str):
    cursor.execute(f"SELECT id, subject, title, created_at FROM homework WHERE token='{token}'")
    return cursor.fetchall()


def get_return_id(user_id: int):
    cursor.execute(f"SELECT id FROM users WHERE user_id={user_id}")
    return cursor.fetchall()


def get_delete_homework(row_id: int):
    cursor.execute(f"DELETE FROM homework WHERE id={row_id}")
    conn.commit()


def get_check_editor_code(token: str):
    cursor.execute(f"SELECT editor_token FROM schools WHERE token='{token}'")
    return cursor.fetchall()


def get_update_user_role(id: int):
    cursor.execute(f"UPDATE users SET role='Редактор' WHERE id={id};")
    conn.commit()
