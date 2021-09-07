# ISCBot. Telegram school helper for students.
# Copyright (C) 2021 Artem Vorochaev (vorochaev2004@live.ru, github.com/Hymiside)
#                    Artem Voronov (mreluzium@mail.ru, github.com/MrEluzium)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import NamedTuple
from datetime import date
import db


class Homework(NamedTuple):
    id: int
    subject: str
    homework: str
    created_at: date


class TokenClassWithID(NamedTuple):
    id: int
    token_class: str


class Timetable(NamedTuple):
    subject: str
    time: str


def check_user_profile(user_id: int):
    all_user_id = db.get_check_user_profile()
    list_user_id = [id for user_id in all_user_id for id in user_id]
    if user_id in list_user_id:
        return True
    else:
        return False


def check_user_role(user_id: int):
    """Возвращает роль пользователя по его user_id"""
    role_not_format = db.get_check_user_role(user_id)
    role = [role for tuple_role in role_not_format for role in tuple_role]
    return role


def add_user_profile(username: str, school_id: int, user_id: int):
    """Добавляет нового пользователя в БД"""
    values = (username, school_id, 'Читатель', user_id)
    db.get_add_user_profile(values)


def add_homework(subject: str, title: str, user_id: int, school_id: int):
    values = (subject, title, user_id, *school_id)
    db.get_add_homework(values)


def view_homework(school_id: int):
    all_homework_not_format = db.get_view_homework(school_id)
    all_homework = [Homework(id=tuple_homework[0], subject=tuple_homework[1], homework=tuple_homework[2],
                             created_at=tuple_homework[3]) for tuple_homework in all_homework_not_format]
    return all_homework


def return_school_id(user_id: int):
    """Возвращает school_id пользователя по его user_id"""
    school_id_ = db.return_school_id(user_id)
    return school_id_


def check_editor_token(school_id: int, input_editor_code: str):
    all_editor_code_not_format = db.get_check_editor_token(school_id)
    all_editor_code = [editor_code for tuple_editor_code in all_editor_code_not_format
                       for editor_code in tuple_editor_code]

    if input_editor_code in all_editor_code:
        return True
    else:
        return False


def return_timetable(day: str, school_id: int):
    timetable_not_format = db.return_timetable_on_day(day, school_id)
    timetable = [Timetable(subject=tuple_timetable[0], time=tuple_timetable[1])
                 for tuple_timetable in timetable_not_format]
    return timetable
