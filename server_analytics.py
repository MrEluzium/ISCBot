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

import time
import logging
import random
import string

from aiogram import Bot, Dispatcher, types, executor

import db_analytics
import server
import keyboard_analytics

bot_ = Bot(token='')
dp = Dispatcher(bot_)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    if message.from_user.id == 599516086:
        await message.answer('📱Для взаимодествия с ботом, используй меню кнопок👇',
                             reply_markup=keyboard_analytics.main_keyboard())
    else:
        await message.answer('Этот бот закрыт от постороннихь глаз!')


@dp.callback_query_handler(text='total_users')
async def total_user(callback_query: types.CallbackQuery):
    total_user_ = db_analytics.get_return_total_users()
    return await callback_query.message.answer(f'Сейчас этот бот использует {len(total_user_)} человек(а)',
                                               reply_markup=keyboard_analytics.main_keyboard())


@dp.callback_query_handler(text='total_homework')
async def total_homework(callback_query: types.CallbackQuery):
    total_homework_ = db_analytics.get_return_total_homework()
    return await callback_query.message.answer(f'Сейчас в боте находится {len(total_homework_)} домашних задания(й)',
                                               reply_markup=keyboard_analytics.main_keyboard())


@dp.callback_query_handler(text='total_class')
async def total_class(callback_query: types.CallbackQuery):
    total_class_ = db_analytics.get_return_total_class()
    return await callback_query.message.answer(f'Сейчас в боте зарегистрировано {len(total_class_)} класс(a/ов)',
                                               reply_markup=keyboard_analytics.main_keyboard())


@dp.callback_query_handler(text='create_newsletter')
async def create_newsletter(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Теперь вводи текст для рассылки, но в начале добавь *')


@dp.message_handler(lambda message: message.text.startswith('*'))
async def input_newsletter(message: types.Message):
    newsletter = message.text.strip('*').strip()

    all_user_id = [user_id for tuple_user_id in db_analytics.get_return_user_id() for user_id in tuple_user_id]
    for user_id in all_user_id:
        await server.bot.send_message(user_id, newsletter)
        time.sleep(0.5)


@dp.callback_query_handler(text='signup_class')
async def signup_class(callback_query: types.CallbackQuery):
    return await callback_query.message.answer('Введи название школы\nШкола: <название>')


@dp.message_handler(lambda message: message.text.startswith('Школа:'))
async def input_school_name(message: types.Message):
    global school_name
    school_name = message.text[7:]
    return await message.answer('Теперь введи свой класс\nКласс: <название>')


@dp.message_handler(lambda message: message.text.startswith('Класс:'))
async def input_class_name(message: types.Message):
    class_name = message.text[7:]

    token = 'token' + ''.join(random.choice(string.ascii_lowercase) for i in range(6))
    editor_token = 'editor' + ''.join(random.choice(string.ascii_lowercase) for i in range(6))
    values = (school_name, class_name, token, editor_token)

    db_analytics.get_signup_class(values)
    return await message.answer('✅Зарегистрирован новый класс\n\n'
                                f'Школа:  {school_name}\nКласс:  {class_name}\nТокен класса:  {token}\nТокен '
                                f'Редактора:  {editor_token}', reply_markup=keyboard_analytics.main_keyboard())


@dp.message_handler()
async def other(message: types.Message):
    return await message.answer('🤷Я тебя не понимаю🤷')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
