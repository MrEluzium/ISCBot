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

import requests

from aiogram import types

from datetime import datetime

now = datetime.now()


def get_day_of_week():
    """Возвращает настоящий день недели"""
    json_data = requests.get('http://worldclockapi.com/api/json/utc/now').json()
    day = json_data["dayOfTheWeek"]
    return day


def main_keyboard():
    list_button = [
        types.InlineKeyboardButton(text="✏️Добавить ДЗ", callback_data='add_homework'),
        types.InlineKeyboardButton(text="📚Посмотреть ДЗ", callback_data='view_homework'),
        types.InlineKeyboardButton(text="📅Посмотреть расписание", callback_data='view_timetable'),
        types.InlineKeyboardButton(text="✈️Создать рассылку", callback_data='create_newsletter'),
        types.InlineKeyboardButton(text="㊙️Ввести код Редактора", callback_data='enter_code'),
        types.InlineKeyboardButton(text="💸Задонатить", callback_data='pay'),
        types.InlineKeyboardButton(text="🚪Выйти", callback_data='logout')]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*list_button)
    return keyboard


def homework_keyboard():
    list_button = [
        types.InlineKeyboardButton(text='Русский язык', callback_data='russian'),
        types.InlineKeyboardButton(text='Литература', callback_data='literature'),
        types.InlineKeyboardButton(text='Алгебра', callback_data='algebra'),
        types.InlineKeyboardButton(text='Геометрия', callback_data='geometry'),
        types.InlineKeyboardButton(text='Физика', callback_data='physics'),
        types.InlineKeyboardButton(text='Информатика', callback_data='informatics'),
        types.InlineKeyboardButton(text='Химия', callback_data='chemistry'),
        types.InlineKeyboardButton(text='Английский язык', callback_data='english'),
        types.InlineKeyboardButton(text='Биология', callback_data='biology'),
        types.InlineKeyboardButton(text='Астрономия', callback_data='astronomy'),
        types.InlineKeyboardButton(text='ОБЖ', callback_data='obg'),
        types.InlineKeyboardButton(text='История', callback_data='history'),
        types.InlineKeyboardButton(text='Физкультура', callback_data='sport'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*list_button)
    return keyboard


def all_schools(schools):
    list_button = [types.InlineKeyboardButton(text=f'🏫{i[1]}  {i[2]}', callback_data=f'cls{i[0]}') for i in schools]
    list_button.append(types.InlineKeyboardButton(text='📝Зарегистрировать класс', callback_data='create_new_class'))
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*list_button)
    return keyboard


def timetable():
    list_button = [
        types.InlineKeyboardButton(text='Сегодня', callback_data=f'{get_day_of_week()}'),
        types.InlineKeyboardButton(text='Понедельник', callback_data='Monday'),
        types.InlineKeyboardButton(text='Вторник', callback_data='Tuesday'),
        types.InlineKeyboardButton(text='Среда', callback_data='Wednesday'),
        types.InlineKeyboardButton(text='Четверг', callback_data='Thursday'),
        types.InlineKeyboardButton(text='Пятница', callback_data='Friday')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*list_button)
    return keyboard
