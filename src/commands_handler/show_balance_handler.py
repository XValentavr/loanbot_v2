from telebot import types

from cruds.earning_cruds import earnings_cruds
from helpers.enums.helper_main_agent_enum import HelperMainAgentEnum
from helpers.enums.paginator_enum import BalancePaginator
from helpers.inform_message_creator.create_balance_message import create_balance_message, create_balance_history
from models.admins import LoanAdminsModel

starter = {'start': BalancePaginator.PAGE.value}


def get_agent_balance(message, loan, agent: LoanAdminsModel):
    """
    Calculate agent balance
    :param message: chat message
    :param loan: bot instance
    :param agent: current agent
    :return:
    """
    starter['start'] = BalancePaginator.PAGE.value

    earnings = earnings_cruds.get_earning_by_agent_id(agent.id)
    message_data = create_balance_message(agent.admin_username, earnings)

    loan.send_message(chat_id=message.chat.id, text=message_data, parse_mode='MarkdownV2', reply_markup=generate_keyboard())


def get_more_agent_balance(message, loan, agent):
    earnings = earnings_cruds.get_earning_by_agent_id(agent.id)
    message_data = create_balance_history(earnings[starter['start'] : starter['start'] + BalancePaginator.PAGE.value], withdraw=None)
    starter['start'] = starter['start'] + BalancePaginator.PAGE.value
    if starter['start'] <= len(earnings):
        loan.send_message(chat_id=message.chat.id, text=message_data, parse_mode='MarkdownV2', reply_markup=generate_keyboard())
    else:
        loan.send_message(chat_id=message.chat.id, text='Конец истории', parse_mode='MarkdownV2')


def generate_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='Показать историю', callback_data=HelperMainAgentEnum.MORE_BALANCE)
    keyboard.add(key)
    return keyboard
