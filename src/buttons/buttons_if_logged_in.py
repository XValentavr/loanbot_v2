from telebot import types

from helpers.enums.inline_buttons_enum import InlineButtonsEnum


def buttons_if_logged_in(message, loan):
    """
    Create buttons fore agent that are already logged in
    :param message: message of chat
    :param loan: current bot instance
    :return: None
    """

    keyboard = types.InlineKeyboardMarkup()
    balance = types.InlineKeyboardButton(text='Баланс', callback_data=InlineButtonsEnum.BALANCE)
    incomes = types.InlineKeyboardButton(text='Мои доходы', callback_data=InlineButtonsEnum.INCOME)
    insert_data = types.InlineKeyboardButton(text='Внести операцию', callback_data=InlineButtonsEnum.INSERT)
    withdraw = types.InlineKeyboardButton(text='Вывести', callback_data=InlineButtonsEnum.WITHDRAWAL)
    keyboard.row(balance, incomes, insert_data, withdraw)

    loan.send_message(message.chat.id, 'Выберите команду', reply_markup=keyboard)
