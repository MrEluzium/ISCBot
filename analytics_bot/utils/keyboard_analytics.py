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

from aiogram import types


def main_keyboard():
    list_button = [
        types.InlineKeyboardButton(text="👪Количество пользователей", callback_data='total_users'),
        types.InlineKeyboardButton(text="📚Количество ДЗ", callback_data='total_homework'),
        types.InlineKeyboardButton(text="👨‍🏫Количество классов", callback_data='total_class'),
        types.InlineKeyboardButton(text="🏫Регистрация класса", callback_data='signup_class')]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*list_button)
    return keyboard
