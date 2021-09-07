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

import sqlite3
from typing import Tuple

conn = sqlite3.connect('../service.db', check_same_thread=False)
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
