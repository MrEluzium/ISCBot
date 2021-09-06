import sqlite3
from typing import Tuple


conn = sqlite3.connect('service.db', check_same_thread=False)
cursor = conn.cursor()


def get_check_user_profile():
    """Возвращает список всех user_id из БД, для проверки наличия пользователя в БД"""
    cursor.execute(f"SELECT user_id FROM users")
    return cursor.fetchall()


def get_check_user_role(user_id: int):
    """Возвращает роль пользователя по его user_id"""
    cursor.execute(f"SELECT role FROM users WHERE user_id={user_id}")
    return cursor.fetchall()


def get_add_user_profile(values: Tuple):
    """Добавление нового пользователя в БД"""
    cursor.execute(f"INSERT INTO users(username, school_id, role, user_id) VALUES(?, ?, ?, ?);", values)
    conn.commit()


def get_add_homework(values: Tuple):
    """Добавляет новое домашнее задание"""
    cursor.execute(f"INSERT INTO homework(subject, title, user_id, school_id) VALUES(?, ?, ?, ?);", values)
    conn.commit()


def get_view_homework(school_id: int):
    """Возвращает все домашнее задание по school_id"""
    cursor.execute(f"SELECT id, subject, title, created_at FROM homework WHERE school_id={school_id}")
    return cursor.fetchall()


def get_delete_homework(row_id: int):
    """Удаляет домашнее задание по его id"""
    cursor.execute(f"DELETE FROM homework WHERE id={row_id}")
    conn.commit()


def get_check_editor_token(school_id: int):
    """Проверяет editor_token по school_id пользователя"""
    cursor.execute(f"SELECT editor_token FROM schools WHERE id={school_id}")
    return cursor.fetchall()


def get_update_user_role(id: int):
    """Повышает роль пользователя с Читателя до Редактора"""
    cursor.execute(f"UPDATE users SET role='Редактор' WHERE id={id};")
    conn.commit()


def return_all_schools():
    """Возвращает все школы в боте для регистрации пользователя"""
    not_format = cursor.execute(f"SELECT id, school_name, class_name FROM schools").fetchall()
    all_schools = [tuple_schools for tuple_schools in not_format]
    return all_schools


def return_school_id(user_id: int):
    """Возвращает school_id пользователя по его user_id"""
    not_format = cursor.execute(f"SELECT school_id FROM users WHERE user_id={user_id}").fetchall()
    school_id = [id for tuple_id in not_format for id in tuple_id]
    return school_id


def return_id_and_school_id(user_id: int):
    """Возвращает id и school_id пользователя по его user_id"""
    not_format = cursor.execute(f"SELECT id, school_id FROM users WHERE user_id={user_id}").fetchall()
    id_and_school_id = [data for tuple_data in not_format for data in tuple_data]
    return id_and_school_id


def get_logout(user_id: int):
    """Удаляет пользователя из БД"""
    cursor.execute(f"DELETE FROM users WHERE user_id={user_id}")
    conn.commit()


def return_all_user_id_my_class(school_id: int):
    """Возвращает все user_id класса пользователя, который вызывал эту функцию"""
    not_format = cursor.execute(f"SELECT user_id FROM users WHERE school_id={school_id}").fetchall()
    all_user_id = [user_id for tuple_user_id in not_format for user_id in tuple_user_id]
    return all_user_id


def return_timetable_on_day(day: str, school_id: int):
    """Возвращает расписание на выбранный день по school_id в рамках класса"""
    timetable = cursor.execute(f"SELECT subject, time FROM timetable WHERE day='{day}' AND school_id={school_id}")
    # timetable = [tuple_timetable for tuple_timetable in not_format]
    return timetable


def add_new_class(values: tuple):
    """Добавляет новый класс в БД"""
    cursor.execute('INSERT INTO schools(school_name, class_name, editor_token) VALUES(?, ?, ?);', values)
    conn.commit()


def init_db():
    """Инициализирует БД"""
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT * FROM sqlite_master")
    table_exists = cursor.fetchall()

    if not table_exists:
        init_db()


check_db_exists()
# print(now.strftime("%A"))
