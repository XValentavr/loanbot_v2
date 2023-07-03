import logging
import telebot

from buttons.buttons_if_logged_in import buttons_if_logged_in
from buttons.buttons_insert_data import buttons_insert_data
from buttons.buttons_my_prev_incomes import buttons_get_previous_incomes
from commands_handler.agent_balances_handler import handler_agent_balances
from commands_handler.agent_xlsx import send_xlsx_file
from commands_handler.show_balance_handler import get_agent_balance
from create_engine import session
from cruds.agent_cruds import agent_cruds
from helpers import creds
from helpers.enums.helper_main_agent_enum import HelperMainAgentEnum

from helpers.event_handler_helper import event_main_buttons_helper
from helpers.decorators.is_logged_in_decorator import login_required

from helpers.check_password import check_password_and_set_privacy
from helpers.withdrawal_helper import withdrawal_helper

loan = telebot.TeleBot(creds.Creds.LOAN_BOT_ID)
logging.basicConfig(filename="sample.log", level=logging.ERROR)


@loan.message_handler(commands=["start"])
def send_welcome(message):
    session.commit()
    agent = agent_cruds.get_by_username(username=message.from_user.username)
    if not agent.is_login:
        loan.send_message(message.chat.id, "Введите пароль")
        loan.register_next_step_handler(message, lambda msg: check_password_and_set_privacy(msg, loan, agent))
    else:
        buttons_if_logged_in(message, loan)


@loan.message_handler(commands=["income"])
@login_required
def my_income(message):
    agent = agent_cruds.get_by_username(username=message.from_user.username)
    buttons_get_previous_incomes(message, loan, agent)


@loan.message_handler(commands=["withdraw"])
@login_required
def my_withdrawal(message):
    agent = agent_cruds.get_by_username(username=message.from_user.username)
    withdrawal_helper(message, loan, agent)


@loan.message_handler(commands=["agents"])
@login_required
def my_income(message):
    agent = agent_cruds.get_by_username(username=message.from_user.username)
    if agent.admin_username in HelperMainAgentEnum.MAIN_ADMIN_USERNAME:
        handler_agent_balances(message, loan, agent)
    else:
        loan.send_message(message.chat.id, "У вас нет доступа к этой команде!")


@loan.message_handler(commands=["sheet"])
@login_required
def sheet_sending(message):
    agent = agent_cruds.get_by_username(username=message.from_user.username)
    if agent.admin_username in HelperMainAgentEnum.MAIN_ADMIN_USERNAME:
        send_xlsx_file(loan, message)
    else:
        loan.send_message(message.chat.id, "У вас нет доступа к этой команде!")


@loan.message_handler(commands=["balance"])
@login_required
def my_balance(message):
    agent = agent_cruds.get_by_username(username=message.from_user.username)
    get_agent_balance(message, loan, agent)


@loan.message_handler(commands=["insert"])
@login_required
def insert_data(message):
    buttons_insert_data(message, loan)


@loan.callback_query_handler(func=lambda call: True)
@login_required
def handle_callback_query_mapper(call):
    agent = agent_cruds.get_by_username(username=call.from_user.username)
    event_main_buttons_helper(call=call, agent=agent, loan=loan)
