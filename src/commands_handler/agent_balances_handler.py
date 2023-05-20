from datetime import date

from buttons.buttons_agents_balances import buttons_all_agents, buttons_agent_history
from cruds.agent_cruds import agent_cruds
from cruds.earning_cruds import earnings_cruds
from helpers.enums.helper_main_agent_enum import HelperMainAgentEnum
from helpers.helper_functions import regex_escaper
from helpers.income_and_profit.profit_last_two_weeks_calculator import create_profit_string, include_withdrawal, \
    create_proportional_parts_of_month, generate_string_for_graded_month
from helpers.income_and_profit.profit_other_date_calculator import get_profit_of_other_dates
from helpers.inform_message_creator.create_balance_message import create_balance_message


def handler_agent_balances(message, loan, agent):
    """
    handler agents
    :param message: current chat message
    :param loan: bot instance
    :param agent: current agent
    :return: None
    """
    agents = agent_cruds.get_agents_to_check_balance(agent)
    buttons_all_agents(message, loan, agents)


def get_agents_balance(message, loan, agent_username):
    """
    Get agents story for main agent
    :param message: message of chat
    :param loan: loan instance
    :param agent_username: main agent
    :param limit: limit of history
    :return: None
    """
    first_part, second_part = create_proportional_parts_of_month()

    agent_to_check = agent_cruds.get_by_username(agent_username)

    earnings = earnings_cruds.get_earning_by_agent_id(agent_to_check.id)

    balance = create_balance_message(earnings, include_history=False)
    all_profits = get_profit_of_other_dates(agent_to_check, calculate_date=False)

    history_first_part = '\n'.join(
        create_incomes_story(get_history(agent_to_check, date_to_check=first_part))) + '\n\n'

    history_second_part = '\n'.join(
        create_incomes_story(get_history(agent_to_check, date_to_check=second_part))) + '\n\n'

    complex_history = generate_string_for_graded_month(history_first_part.strip(), history_second_part.strip(),
                                                       for_main_agent=True)

    message_of_agent = create_message(balance, all_profits, complex_history.strip())

    buttons_agent_history(message, loan, message_of_agent)


def get_more_history(message, loan, agent_username, start, end):
    """
    Get history if there are more then 10 transactions
    :param message: chat message
    :param loan: current bot instance
    :param agent_username: agent to get history of
    :param limit: limit of transactions
    :return: None
    """
    agent_to_check = agent_cruds.get_by_username(agent_username)

    today = date.today()
    first_day_of_current_month = date(today.year, today.month, 1)

    history = '\n'.join(create_incomes_story(get_history(agent_to_check, first_day_of_current_month, start, end)))
    if len(history) > int(HelperMainAgentEnum.LIMIT):
        buttons_agent_history(message, loan, history)
    else:
        loan.send_message(chat_id=message.chat.id, text='Больше ничего не найдено')


def create_message(balance, all_profits, history):
    """
    Create message of initial request by main admin
    :param balance: balance of agent
    :param all_profits: profit of agent
    :param history: comments of
    :return:
    """
    return f'{balance}\n{all_profits}\n\n\n{history}'


def get_history(agent, date_to_check, start=0, end=int(HelperMainAgentEnum.LIMIT), ):
    """
    Get earnings history of transactions
    :param agent:
    :param start:
    :param end:
    :return:
    """
    return earnings_cruds.get_earnings_history_by_date(agent.id, start=start, end=end, date_to_check=date_to_check)


def create_incomes_story(earnings):
    """
    Create special string for incomes
    :param earnings:
    :return:
    """
    return [create_profit_string(profit, for_main_admin=True) for profit in earnings]


def get_withdrawal_string(withdrawal):
    return [f'***{regex_escaper(include_withdrawal(withdraw))}***' for withdraw in withdrawal]
