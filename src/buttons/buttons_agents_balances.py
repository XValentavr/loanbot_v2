from typing import List

from telebot import types

from helpers.enums.helper_enum import HelperEnum
from models.admins import LoanAdminsModel


def buttons_all_agents(message, loan, agents: List[LoanAdminsModel]):
    """
    Create buttons fore agent with income sources
    :param message: message of chat
    :param loan: current bot instance
    :param agents: all possible agents
    :return: None
    """
    agent_usernames = sorted([agent.admin_username for agent in agents])

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    for name in agent_usernames:
        key = types.InlineKeyboardButton(text=name, callback_data=name)
        keyboard.add(key)

    loan.send_message(chat_id=message.chat.id, text="Пользователи", reply_markup=keyboard)


def buttons_agent_history(message, loan, message_data):
    """
    Create buttons fore agent with income sources
    :param message: message of chat
    :param loan: current bot instance
    :param message_data: вata abount agent
    :return: None
    """
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='Показать историю', callback_data=HelperEnum.MORE_HISTORY)
    keyboard.add(key)
    loan.send_message(chat_id=message.chat.id, text=message_data, reply_markup=keyboard, parse_mode='MarkdownV2')
