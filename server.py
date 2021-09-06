import time
import logging
import random
import string

from aiogram import Bot, Dispatcher, types, executor

import keyboard
import logic
import db

bot = Bot(token='')
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands='menu')
@dp.message_handler(commands='start')
async def new_send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_status = logic.check_user_profile(user_id)

    if user_status:
        await message.answer('📱Для взаимодествия с ботом, используй меню кнопок👇',
                             reply_markup=keyboard.main_keyboard())

    elif not user_status:
        username = message.from_user.username
        if username is not None:
            await message.answer(
                f'🙋‍♂️Привет, {username}!\nНажми на кнопку класса в котором ты учишься. Если твоего класса'
                f' нет в списке — нажми кнопку зарегистрировать класс и следуй инструкции.',
                reply_markup=keyboard.all_schools())
        else:
            await message.answer(
                f'🙋‍♂️Привет!\nНажми на кнопку класса в котором ты учишься. Если твоего класса'
                f' нет в списке — нажми кнопку зарегистрировать класс и следуй инструкции.',
                reply_markup=keyboard.all_schools())


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('cls'))
async def registration(callback_query: types.CallbackQuery):
    """Регистрируем пользователя"""
    school_id = int(callback_query.data[3:])
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username

    logic.add_user_profile(username, school_id, user_id)
    return await callback_query.message.answer(
        '🤍Спасибо за регистрацию!🤍\n\n📱Для взаимодействия с ботом, используй меню кнопок👇',
        reply_markup=keyboard.main_keyboard())


@dp.callback_query_handler(text='add_homework')
async def add_homework(callback_query: types.CallbackQuery):
    """Ловим коллбэк и определяем может ли пользователь добавлять ДЗ"""
    user_id = callback_query.from_user.id
    role = logic.check_user_role(user_id)

    if role == ['Редактор']:
        await callback_query.message.answer('📖Нажми на кнопку меню, чтобы добавить домашнее задание по выбранному '
                                            'предмету👇', reply_markup=keyboard.homework_keyboard())

    elif role == ['Читатель']:
        await callback_query.message.answer('🙅‍♂️Твой уровень — Читатель🙅‍♂️\nДобавить ДЗ может только Редактор!'
                                            ' Чтобы повысить уровень, нажми на кнопку "Ввести код Редактора" и '
                                            'введи код Редактора. Если возникли проблемы, обратись к @hymiside.',
                                            reply_markup=keyboard.main_keyboard())

    elif not role:
        await callback_query.message.answer('❗Ты не зарегистрирован или удален❗\n Нажми /start, чтобы '
                                            'зарегистрироваться.')


@dp.callback_query_handler(text='russian')
@dp.callback_query_handler(text='literature')
@dp.callback_query_handler(text='algebra')
@dp.callback_query_handler(text='geometry')
@dp.callback_query_handler(text='physics')
@dp.callback_query_handler(text='informatics')
@dp.callback_query_handler(text='chemistry')
@dp.callback_query_handler(text='english')
@dp.callback_query_handler(text='biology')
@dp.callback_query_handler(text='astronomy')
@dp.callback_query_handler(text='obg')
@dp.callback_query_handler(text='history')
@dp.callback_query_handler(text='sport')
async def input_subject(callback_query: types.CallbackQuery):
    """Ловим коллбэк с предметом и кладем его в глобальную переменную, чтобы потом его записать в БД"""
    global subject

    user_id = callback_query.from_user.id
    school_id = logic.return_school_id(user_id)

    if not school_id:
        return await callback_query.message.answer('❗Ты не зарегистрирован или удален❗\n Нажми /start, чтобы '
                                                   'зарегистрироваться.')

    subjects_dict = {
        'russian': 'Русский язык',
        'literature': 'Литература',
        'algebra': 'Алгебра',
        'chemistry': 'Химия',
        'english': 'Английский язык',
        'geometry': 'Геометрия',
        'informatics': 'Информатика',
        'physics': 'Физика',
        'sport': 'Физкультура',
        'biology': 'Биология',
        'astronomy': 'Астрономия',
        'history': 'История',
        'obg': 'ОБЖ'
    }
    subject_key = callback_query.data
    subject = subjects_dict[subject_key]
    await callback_query.message.answer('💁‍♂️Теперь вводи домашнее задание, но в начале добавь *')


@dp.message_handler(lambda message: message.text.startswith('*'))
async def input_homework(message: types.Message):
    """Получаем текст домашенего задания и записываем его в БД"""
    user_id = message.from_user.id
    homework = message.text.strip('*').strip()

    school_id = logic.return_school_id(user_id)
    logic.add_homework(subject, homework, user_id, school_id)
    return await message.answer('✅Домашнее задание добавлено', reply_markup=keyboard.main_keyboard())


@dp.callback_query_handler(text='view_homework')
async def view_homework(callback_query: types.CallbackQuery):
    """Выводим домашнее задание класса пользователя"""
    user_id = callback_query.from_user.id
    user_status = logic.check_user_profile(user_id)
    if not user_status:
        return await callback_query.message.answer('❗Ты не зарегистрирован или удален❗\n Нажми /start, чтобы '
                                                   'зарегистрироваться.')
    school_id = logic.return_school_id(user_id)
    all_homework = logic.view_homework(*school_id)

    if not all_homework:
        return await callback_query.message.answer('📖Домашнего задания нет📖\nКайфуй🤍',
                                                   reply_markup=keyboard.main_keyboard())

    list_homework = [
        f'Предмет: {homework.subject}\nЗадание: {homework.homework}\nЗаписано: '
        f'{homework.created_at.split("-")[2]}.{homework.created_at.split("-")[1]}.{homework.created_at.split("-")[0]} '
        f'- чтобы удалить, нажми /delete{homework.id}' for homework in all_homework]

    return await callback_query.message.answer('📖Домашнее задание📖\n\n' + "\n\n".join(list_homework),
                                               reply_markup=keyboard.main_keyboard())


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def delete_homework(message: types.Message):
    """Удаляем домашнее задание"""
    user_id = message.from_user.id
    role = logic.check_user_role(user_id)

    if role == ['Редактор']:
        row_id = int(message.text[7:])
        db.get_delete_homework(row_id)
        return await message.answer('✅Домашнее задание удалено', reply_markup=keyboard.main_keyboard())

    elif role == ['Читатель']:
        return await message.answer('🙅‍♂️Твой уровень — Читатель🙅‍♂️\nУдалить ДЗ может только Редактор!'
                                    ' Чтобы повысить уровень, нажми на кнопку "Ввести код Редактора" и '
                                    'введи код Редактора. Если возникли проблемы, обратись к @hymiside.',
                                    reply_markup=keyboard.main_keyboard())

    elif not role:
        return await message.answer('❗Ты не зарегистрирован или удален❗\n Нажми /start, чтобы '
                                    'зарегистрироваться.')


@dp.callback_query_handler(text='enter_code')
async def enter_editor_token(callback_query: types.CallbackQuery):
    """Ловим коллбэк и определяем нужна ли парню такая машина"""
    user_id = callback_query.from_user.id
    role = logic.check_user_role(user_id)

    if role == ['Читатель']:
        await callback_query.message.answer('💁‍♂️Теперь вводи код Редактора')

    elif role == ['Редактор']:
        return await callback_query.message.answer('🙅‍♂️Твой уровень — Редактор🙅‍♂️\n Дальше только БОГ, но это не '
                                                   'ко мне)', reply_markup=keyboard.main_keyboard())

    elif not role:
        return await callback_query.message.answer('❗Ты не зарегистрирован или удален❗\n Нажми /start, чтобы '
                                                   'зарегистрироваться.')


@dp.message_handler(lambda message: message.text.startswith('editor'))
async def input_editor_token(message: types.Message):
    """Ловим токен редактора и проверяем его на правильность, если все норм,
    то повышаем звание, если нет - петушим"""
    user_id = message.from_user.id
    editor_token = message.text

    data = db.return_id_and_school_id(user_id)
    id = data[0]
    school_id = data[1]
    status_editor_token = logic.check_editor_token(school_id, editor_token)

    if status_editor_token:
        db.get_update_user_role(id)
        return await message.answer('✅Твой уровень повышен до Редактора✅\n\n'
                                    'Теперь ты можешь добавлять и удалять ДЗ, а также создавать различные '
                                    'ивенты', reply_markup=keyboard.main_keyboard())

    elif not status_editor_token:
        return await message.answer('🛑Такого кода Редактора не существует. Обратись к @hymiside.🛑')


@dp.callback_query_handler(text='pay')
async def donate(callback_query: types.CallbackQuery):
    """Гыыыыы, донатики"""
    button = types.InlineKeyboardButton(text="Помочь с деньгами", url='https://yoomoney.ru/to/4100117051898846')
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(button)

    return await callback_query.message.answer('Сейчас я содержу бота на свои накопления, но ты можешь помочь — '
                                               'задонатить на оплату сервера, маркетинг, создание контента и '
                                               'дальнейшее развитие бота!\n\n'
                                               '🤍Спасибо, что пользуешься Домашка.Бот🤍', reply_markup=keyboard)


@dp.callback_query_handler(text='logout')
async def logout(callback_query: types.CallbackQuery):
    """Пользователь выходит из класса и бот удаляет его из БД"""
    user_id = callback_query.from_user.id
    db.get_logout(user_id)
    return await callback_query.message.answer('✅Ты успешно вышел из своего класса✅\nЧтобы снова начать пользоваться '
                                               'ботом — нажми /start.')


@dp.callback_query_handler(text='create_newsletter')
async def create_newsletter(callback_query: types.CallbackQuery):
    """Создает рассылку внутри класса"""
    user_id = callback_query.from_user.id
    role = logic.check_user_role(user_id)

    if role == ['Редактор']:
        await callback_query.message.answer('💁‍♂️Теперь вводи текст для рассылки, но в начале добавь &')

    elif role == ['Читатель']:
        return await callback_query.message.answer(
            '🙅‍♂️Твой уровень — Читатель🙅‍♂️\nСоздать рассылку может только Редактор!'
            ' Чтобы повысить уровень, нажми на кнопку "Ввести код Редактора" и '
            'введи код Редактора. Если возникли проблемы, обратись к @hymiside.',
            reply_markup=keyboard.main_keyboard())
    elif not role:
        return await callback_query.message.answer('❗Ты не зарегистрирован или удален❗\n Нажми /start, чтобы '
                                                   'зарегистрироваться.')


@dp.message_handler(lambda message: message.text.startswith('&'))
async def input_newsletter(message: types.Message):
    """Вводим текст для рассылки и отправляем её"""
    newsletter = message.text.strip('&').strip()
    user_id = message.from_user.id
    school_id = db.return_school_id(user_id)

    all_user_id_my_class = db.return_all_user_id_my_class(*school_id)
    for user_id in all_user_id_my_class:
        await bot.send_message(user_id, newsletter)
        time.sleep(0.5)


@dp.callback_query_handler(text='view_timetable')
async def enter_timetable(callback_query: types.CallbackQuery):
    return await callback_query.message.answer('Выбери на какой день ты хочешь посмотреть расписание и нажми на'
                                               ' кнопку🔘',
                                               reply_markup=keyboard.timetable())


@dp.callback_query_handler(text='Monday')
@dp.callback_query_handler(text='Tuesday')
@dp.callback_query_handler(text='Wednesday')
@dp.callback_query_handler(text='Thursday')
@dp.callback_query_handler(text='Friday')
@dp.callback_query_handler(text='Saturday')
@dp.callback_query_handler(text='Sunday')
async def watch_timetable(callback_query: types.CallbackQuery):
    list_day = {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
    }

    user_id = callback_query.from_user.id
    role = logic.check_user_role(user_id)
    if not role:
        return await callback_query.message.answer('❗Ты не зарегистрирован или удален❗\n Нажми /start, чтобы '
                                                   'зарегистрироваться.')

    day = callback_query.data
    if day == 'Saturday' or day == 'Sunday':
        return await callback_query.message.answer('Сегодня выходной💁‍♂️📆',
                                                   reply_markup=keyboard.main_keyboard())
    school_id = db.return_school_id(user_id)

    all_timetable = logic.return_timetable(day, *school_id)
    count = 1
    list_timetable = []
    if not all_timetable:
        return await callback_query.message.answer('🙅‍♂️У тебя еще нет расписания🙅‍♂️\nНо не переживай, оно скоро '
                                                   'появится.', reply_markup=keyboard.main_keyboard())

    for timetable in all_timetable:
        list_timetable.append(f'{count}. {timetable.subject}  {timetable.time}')
        count += 1

    return await callback_query.message.answer(f'📌Расписание на {list_day[day]}📌\n\n' + "\n".join(list_timetable),
                                               reply_markup=keyboard.main_keyboard())


@dp.callback_query_handler(text='create_new_class')
async def create_new_class(callback_query: types.CallbackQuery):
    return await callback_query.message.answer("<b>Введи название школы в формате</b>\nШкола: "
                                               "«название»\n\n<b>Пример</b>\nШкола: Школа 153",
                                               parse_mode=types.ParseMode.HTML)


@dp.message_handler(lambda message: message.text.startswith('Школа:'))
async def input_school_name(message: types.Message):
    global school_name
    school_name = message.text[7:].strip()
    return await message.answer("<b>Теперь введи свой класс в формате</b>\nКласс: «название»\n\n<b>Пример</b>\nКласс: "
                                "9Б", parse_mode=types.ParseMode.HTML)


@dp.message_handler(lambda message: message.text.startswith('Класс:'))
async def input_class_name(message: types.Message):
    class_name = message.text[7:].strip()

    editor_token = 'editor' + ''.join(random.choice(string.ascii_lowercase) for i in range(6))
    values = (school_name, class_name, editor_token)
    db.add_new_class(values)

    return await message.answer('✅Твой класс зарегистрирован\n\n'
                                f'<b>Код Редактора: {editor_token}.</b> Этот код понадобится тебе чтобы повысить '
                                f'уровень пользователя до Редактора, после этого ты сможешь добавлять домашнее задание '
                                f'и создавать рассылки.\nНажми /start чтобы войти.', parse_mode=types.ParseMode.HTML)


@dp.message_handler()
async def other(message: types.Message):
    """Отлавливаем всякий текст из сообщений и типо не распознаем его"""
    return await message.answer('🤷Я тебя не понимаю🤷\nEcли возникли проблемы обратись к @hymiside.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
