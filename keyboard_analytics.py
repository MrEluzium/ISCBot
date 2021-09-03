from aiogram import types


def main_keyboard():
    list_button = [
        types.InlineKeyboardButton(text="👪Количество пользователей", callback_data='total_users'),
        types.InlineKeyboardButton(text="📚Количество ДЗ", callback_data='total_homework'),
        types.InlineKeyboardButton(text="👨‍🏫Количество классов", callback_data='total_class'),
        types.InlineKeyboardButton(text="✏️Создать рассылку", callback_data='create_newsletter'),
        types.InlineKeyboardButton(text="🏫Регистрация класса", callback_data='signup_class')]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*list_button)
    return keyboard
