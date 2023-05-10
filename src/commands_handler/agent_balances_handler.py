from buttons.buttons_agents_balances import buttons_all_agents, buttons_agent_history
from cruds.agent_cruds import agent_cruds
from cruds.earning_cruds import earnings_cruds
from helpers.enums.helper_enum import HelperEnum
from helpers.income_and_profit.profit_last_two_weeks_calculator import create_profit_string
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
    agent_to_check = agent_cruds.get_by_username(agent_username)

    earnings = earnings_cruds.get_earning_by_agent_id(agent_to_check.id)

    balance = create_balance_message(earnings, include_history=False)
    all_profits = get_profit_of_other_dates(agent_to_check, calculate_date=False)

    history = '\n'.join(create_incomes_story(get_history(agent_to_check, start=0, end=int(HelperEnum.LIMIT))))

    message_of_agent = create_message(balance, all_profits, history)

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

    history = '\n'.join(create_incomes_story(get_history(agent_to_check, start, end)))
    if len(history) > int(HelperEnum.LIMIT):
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


def get_history(agent, start, end):
    """
    Get earnings history of transactions
    :param agent:
    :param start:
    :param end:
    :return:
    """
    return earnings_cruds.get_earnings_history(agent.id, start=start, end=end)


def create_incomes_story(earnings):
    """
    Create special string for incomes
    :param earnings:
    :return:
    """
    return [create_profit_string(profit, for_main_admin=True) for profit in earnings]
