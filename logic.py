from typing import NamedTuple

import db


class Homework(NamedTuple):
    id: int
    subject: str
    homework: str
    created_at: str


class TokenClassWithID(NamedTuple):
    id: int
    token_class: str


def check_user_profile(user_id: int):
    all_user_id = db.get_check_user_profile()
    list_user_id = [id for user_id in all_user_id for id in user_id]
    if user_id in list_user_id:
        return True
    else:
        return False


def check_user_role(user_id: int):
    role_not_format = db.get_check_user_role(user_id)
    role = [role for tuple_role in role_not_format for role in tuple_role]
    return role


def check_token(token: str):
    all_class_token = [class_token for tuple_class_token in db.get_check_class_token() for class_token in
                       tuple_class_token]
    if token in all_class_token:
        return True
    else:
        return False


def add_user_profile(username: str, token: str, user_id: int):
    school_id = [id for tuple_id in db.get_check_school_id(token) for id in tuple_id]
    values = (username, *school_id, 'Читатель', user_id)
    db.get_add_user_profile(values)


def return_token(user_id: int):
    """Возвращает токен"""
    school_id = [id for tuple_school_id in db.get_return_school_id(user_id)
                 for id in tuple_school_id]

    token = [token_ for tuple_token in db.get_return_token(*school_id) for token_ in tuple_token]
    return token


def return_id(user_id: int):
    """Возвращает id пользователя"""
    id = [id_ for tuple_id in db.get_return_id(user_id) for id_ in tuple_id]
    return id


def add_homework(subject: str, title: str, user_id: int, token: str):
    values = (subject, title, user_id, *token)
    db.get_add_homework(values)


def view_homework(token: str):
    all_homework_not_format = db.get_view_homework(token)
    all_homework = [Homework(id=tuple_homework[0], subject=tuple_homework[1], homework=tuple_homework[2],
                             created_at=tuple_homework[3]) for tuple_homework in all_homework_not_format]
    return all_homework


def delete_homework(row_id: int):
    db.get_delete_homework(row_id)


def check_editor_token(token: str, input_editor_code: str):
    all_editor_code_not_format = db.get_check_editor_code(token)
    all_editor_code = [editor_code for tuple_editor_code in all_editor_code_not_format
                       for editor_code in tuple_editor_code]

    if input_editor_code in all_editor_code:
        return True
    else:
        return False


def update_user_role(id: int):
    db.get_update_user_role(id)
