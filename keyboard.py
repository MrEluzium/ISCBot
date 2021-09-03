from aiogram import types


def main_keyboard():
    list_button = [
        types.InlineKeyboardButton(text="✏️Добавить ДЗ", callback_data='add_homework'),
        types.InlineKeyboardButton(text="📚Посмотреть ДЗ", callback_data='view_homework'),
        types.InlineKeyboardButton(text="👨‍🏫Предметы и учителя", callback_data='view_subjects'),
        types.InlineKeyboardButton(text="📅Посмотреть расписание", callback_data='view_schedule'),
        types.InlineKeyboardButton(text="㊙️Ввести код Редактора", callback_data='enter_code'),
        types.InlineKeyboardButton(text="💸Задонатить", callback_data='pay')]
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
