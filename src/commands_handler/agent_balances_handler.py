import datetime

from buttons.buttons_agents_balances import buttons_all_agents, buttons_agent_history
from buttons.buttons_back import buttons_back
from cruds.agent_cruds import agent_cruds
from cruds.earning_cruds import earnings_cruds
from cruds.withdrawal_cruds import withdraw_cruds
from helpers.enums.helper_main_agent_enum import HelperMainAgentEnum
from helpers.helper_functions import regex_escaper
from helpers.income_and_profit.profit_last_two_weeks_calculator import create_profit_string, include_withdrawal, \
    create_proportional_parts_of_month, generate_string_for_graded_month, date_changer
from helpers.income_and_profit.profit_other_date_calculator import get_profit_of_other_dates
from helpers.inform_message_creator.create_balance_message import create_balance_message

agent_username_mapper = {
    'skv_katya': '***Катя***',
    'Klepikovevgenij': '***Евгений***',
    'Valentavr': '1122'
}


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


def get_agents_balance(message, loan, agent_username, current_month_year=None):
    """
    Get agents story for main agent
    :param message: message of chat
    :param loan: loan instance
    :param agent_username: main agent
    :param limit: limit of history
    :return: None
    """
    current_month = datetime.datetime.now().strftime("%B")
    is_current_month = True

    if current_month_year:
        is_current_month = True if current_month == current_month_year['month'] else False

    first_part, second_part = create_proportional_parts_of_month(month=current_month_year)

    agent_to_check = agent_cruds.get_by_username(agent_username)

    withdraw = withdraw_cruds.get_all_by_agent_id_and_time(agent=agent_to_check, date_to_check=None,
                                                           current_month=first_part[0].strftime("%B") or current_month)

    earnings = earnings_cruds.get_earning_by_agent_id(agent_to_check.id)

    balance = create_balance_message(agent_username, earnings, include_history=False)

    profits_first_part = get_profit_of_other_dates(agent_to_check, calculate_date=False, partial=first_part)
    history_first_part = profits_first_part + '\n\n' + '\n'.join(
        create_incomes_story(get_history(agent_to_check, date_to_check=first_part))) + '\n\n'

    profits_second_part = get_profit_of_other_dates(agent_to_check, calculate_date=False, partial=second_part)
    history_second_part = profits_second_part + '\n\n' + '\n'.join(
        create_incomes_story(get_history(agent_to_check, date_to_check=second_part))) + '\n\n'

    complex_history = generate_string_for_graded_month(history_first_part.strip(), history_second_part.strip(),
                                                       for_main_agent=True, months=current_month_year)
    message_of_agent = agent_username_mapper.get(agent_username) + '\n\n' + create_message(balance,
                                                                                           complex_history.strip())

    if is_current_month or ('пока нет' not in history_first_part or 'пока нет' not in history_second_part):
        buttons_agent_history(message, loan, message_of_agent + create_withdraw_string(withdraw))
    else:
        loan.send_message(message.chat.id, "Больше ничего не найдено", reply_markup=buttons_back())


def get_more_history(message, loan, agent_username, current_month_year):
    """
    Get history if there are more then 10 transactions
    :param message: chat message
    :param loan: current bot instance
    :param agent_username: agent to get history of
    :return: None
    """
    get_agents_balance(message, loan, agent_username, current_month_year)


def create_message(balance, history):
    """
    Create message of initial request by main admin
    :param balance: balance of agent
    :param all_profits: profit of agent
    :param history: comments of
    :return:
    """
    return f'{balance}\n\n{history}'


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


def create_withdraw_string(withdraw):
    wtdrw = []
    if withdraw:
        wtdrw.append('\n\n***Запрошено на вывод***\n')
        for w in withdraw:
            wtdrw.append(
                f'{date_changer(str(w.time_created))}: запрошено на вывод {round(int(w.summa), 2)}$')

    return '\n'.join(wtdrw)
