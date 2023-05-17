from telebot import types

from helpers.enums.helper_main_agent_enum import HelperMainAgentEnum


def buttons_main_agents_commands(message, loan):
    """
    Create buttons fore agent with income sources
    :param message: message of chat
    :param loan: current bot instance
    :param agents: all possible agents
    :return: None
    """
    keyboard = types.InlineKeyboardMarkup()
    earnings = types.InlineKeyboardButton(text='Баланс', callback_data=HelperMainAgentEnum.MAIN_AGENT_HISTORY)
    expense = types.InlineKeyboardButton(text='Долг', callback_data=HelperMainAgentEnum.MAIN_AGENT_WITHDRAW)
    keyboard.row(earnings, expense)

    loan.send_message(chat_id=message.chat.id, text="Выберите команду", reply_markup=keyboard)
