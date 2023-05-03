from telebot import types

from helpers.enums.inline_buttons_enum import InlineButtonsEnum


def buttons_insert_data(message, loan):
    """
    Create buttons for insert command
    :param message: chat message
    :param loan: current bot instance
    :return: None
    """
    keyboard = types.InlineKeyboardMarkup()
    earnings = types.InlineKeyboardButton(text='Доходы', callback_data=InlineButtonsEnum.EARNINGS)
    expense = types.InlineKeyboardButton(text='Расходы', callback_data=InlineButtonsEnum.EXPENSE)
    keyboard.row(earnings, expense)

    loan.send_message(message.chat.id, 'Выберите команду', reply_markup=keyboard)
