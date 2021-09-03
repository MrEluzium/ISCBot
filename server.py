import logging

from aiogram import Bot, Dispatcher, types, executor

import keyboard
import logic

bot = Bot(token='')
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands='menu')
@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_status = logic.check_user_profile(user_id)

    if user_status:
        await message.answer('📱Для взаимодествия с ботом, используй меню кнопок👇',
                             reply_markup=keyboard.main_keyboard())

    elif not user_status:
        username = message.from_user.username
        await message.answer(f'🙋‍♂️Привет, {username}!\nТы тут впервые, поэтому нужно зарегистрироваться.'
                             f' Введи токен своего класса. Если его нет обратись к @hymiside.')


@dp.message_handler(lambda message: message.text.startswith('class'))
async def input_class_token(message: types.Message):
    user_id = message.from_user.id
    token = message.text
    username = message.from_user.username

    token_status = logic.check_token(token)

    if token_status:
        logic.add_user_profile(username, token, user_id)
        return await message.answer(
            '🤍Спасибо за регистрацию!🤍\n\n📱Для взаимодействия с ботом, используй меню кнопок👇',
            reply_markup=keyboard.main_keyboard())

    elif not token_status:
        return await message.answer('🛑Такого токена не существует. Обратись к @hymiside.🛑')


@dp.callback_query_handler(text='add_homework')
async def add_homework(callback_query: types.CallbackQuery):
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
    global subject

    user_id = callback_query.from_user.id
    class_token = logic.return_token(user_id)

    if not class_token:
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
    user_id = message.from_user.id
    homework = message.text.strip('*').strip()

    token = logic.return_token(user_id)
    logic.add_homework(subject, homework, user_id, token)
    return await message.answer('✅Домашнее задание добавлено', reply_markup=keyboard.main_keyboard())


@dp.callback_query_handler(text='view_homework')
async def view_homework(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    token = logic.return_token(user_id)

    if not token:
        return await callback_query.message.answer('❗Ты не зарегистрирован или удален❗\n Нажми /start, чтобы '
                                                   'зарегистрироваться.')

    all_homework = logic.view_homework(*token)
    if not all_homework:
        return await callback_query.message.answer('📖Домашнего задания нет📖\nКайфуй🤍',
                                                   reply_markup=keyboard.main_keyboard())

    list_homework = [
        f'Предмет: {homework.subject}\nЗадание: {homework.homework}\nСоздано: {homework.created_at} - чтобы ' \
        f'удалить, нажми /delete{homework.id}' for homework in all_homework]

    return await callback_query.message.answer('📖Домашнее задание📖\n\n' + "\n\n".join(list_homework),
                                               reply_markup=keyboard.main_keyboard())


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def delete_homework(message: types.Message):
    user_id = message.from_user.id
    role = logic.check_user_role(user_id)

    if role == ['Редактор']:
        row_id = int(message.text[7:])
        logic.delete_homework(row_id)
        return await message.answer('✅Домашнее задание удалено', reply_markup=keyboard.main_keyboard())

    elif role == ['Читатель']:
        return await message.answer('🙅‍♂️Твой уровень — Читатель🙅‍♂️\nУдалить ДЗ может только Редактор!'
                                    ' Чтобы повысить уровень, нажми на кнопку "Ввести код Редактора" и '
                                    'введи код Редактора. Если возникли проблемы, обратись к @hymiside.',
                                    reply_markup=keyboard.main_keyboard())

    elif not role:
        return await message.answer('❗Ты не зарегистрирован или удален❗\n Нажми /start, чтобы '
                                    'зарегистрироваться.')


@dp.callback_query_handler(text='view_subjects')
async def view_subjects(message: types.Message):
    pass


@dp.callback_query_handler(text='view_schedule')
async def view_schedule(message: types.Message):
    pass


@dp.callback_query_handler(text='enter_code')
async def enter_editor_code(callback_query: types.CallbackQuery):
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
    user_id = message.from_user.id
    editor_token = message.text

    token = logic.return_token(user_id)
    id = logic.return_id(user_id)
    status_editor_token = logic.check_editor_token(*token, editor_token)

    if status_editor_token:
        logic.update_user_role(*id)
        return await message.answer('✅Твой уровень повышен до Редактора✅\n\n'
                                    'Теперь ты можешь добавлять и удалять ДЗ, а также создавать различные '
                                    'ивенты', reply_markup=keyboard.main_keyboard())

    elif not status_editor_token:
        return await message.answer('🛑Такого кода Редактора не существует. Обратись к @hymiside.🛑')


@dp.callback_query_handler(text='pay')
async def donate(callback_query: types.CallbackQuery):
    button = types.InlineKeyboardButton(text="Помочь с деньгами", url='https://yoomoney.ru/to/4100117051898846')
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(button)

    return await callback_query.message.answer('Сейчас я содержу бота на свои накопления, но ты можешь помочь — '
                                               'задонатить на оплату сервера, маркетинг, создание контента и '
                                               'дальнейшее развитие бота!\n\n'
                                               '🤍Спасибо, что пользуешься Домашка.Бот🤍', reply_markup=keyboard)


@dp.message_handler()
async def other(message: types.Message):
    return await message.answer('🤷Я тебя не понимаю🤷\nEcли возникли проблемы обратись к @hymiside.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
