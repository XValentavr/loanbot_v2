from telebot import types

from helpers.enums.inline_buttons_enum import InlineButtonsEnum


def buttons_back():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    key = types.InlineKeyboardButton(text="Вернуться назад", callback_data=InlineButtonsEnum.BACK)
    keyboard.add(key)

    return keyboard
