import re
from typing import List, Dict

from cruds.agent_cruds import agent_cruds
from cruds.withdrawal_cruds import withdraw_cruds
from helpers.enums.currency_enum import CurrencyEnum
from helpers.enums.paginator_enum import BalancePaginator
from helpers.helper_functions import regex_escaper
from models.earning_model import EarningsModel
from prettytable import PrettyTable

from models.withdraw_model import WithdrawModel


def create_balance_message(agent_username, earnings, include_history=True):
    """
    Create pretty table to chat
    :param earnings: current agent earnings
    :param include_history: s
    :return: changed string
    """
    table = PrettyTable(['Валюта', 'Баланс'])
    agent = agent_cruds.get_by_username(agent_username)
    withdraw = withdraw_cruds.get_all_by_agent_id_and_time(agent, date_to_check=None)

    balances = create_balance(earnings, withdraw=withdraw)
    history = create_balance_history(earnings[0:BalancePaginator.PAGE.value], withdraw=withdraw)
    if balances or history:
        for currency, balance in balances.items():
            table.add_row([currency, balance])
        if include_history:
            return '```{}```'.format(table) + '\n' + history
        return '```{}```'.format(table)
    return 'Баланса пока нет'


def dollar_calculator(earnings: List[EarningsModel]):
    return round(sum([float(earn.summa) for earn in earnings if earn.currency == CurrencyEnum.DOLLAR]), 2)


def eur_calculator(earnings: List[EarningsModel]):
    return str(round(sum([float(earn.summa) for earn in earnings if earn.currency == CurrencyEnum.EURO]), 2)).replace(
        '.', ',')


def uah_calculator(earnings: List[EarningsModel]):
    return str(round(sum([float(earn.summa) for earn in earnings if earn.currency == CurrencyEnum.UAH]), 2)).replace(
        '.', ',')


def create_balance(earnings, withdraw: List = [0.0]) -> Dict:
    """
    Create dict of currency and balance
    :param earnings: agent earnings
    :param withdraw: withdraw summa
    :return: dict of currency and balance
    """
    balance = {}

    dollar = dollar_calculator(earnings)
    eur = eur_calculator(earnings)
    uah = uah_calculator(earnings)
    balance['USD'] = str(float(dollar) - float(sum([float(w.summa) for w in withdraw]))).replace('.', ',')

    balance['EUR'] = eur

    balance['UAH'] = uah

    return balance


def create_balance_history(profits: List[EarningsModel], withdraw: List[WithdrawModel]):
    from helpers.income_and_profit.profit_last_two_weeks_calculator import date_changer

    history = []

    if withdraw:
        history.append('***Выведено***\n')
        for w in withdraw:
            history.append(f'{date_changer(str(w.time_created))}: запрошено на вывод {round(int(w.summa), 2)}$')
        history.append('\n')
    history.append('***История***\n')

    for number, profit in enumerate(profits):
        history.append(history_template(profit, number))

    return '\n'.join(history)


def history_template(profit: EarningsModel, number):
    from helpers.income_and_profit.profit_last_two_weeks_calculator import date_changer

    return regex_escaper(f"{number + 1}. {date_changer(str(profit.time_created))}: ") + f"{escaper(profit)}"


def escaper(profit):
    checked = check_if_float(profit.summa)
    comment = profit.comment.replace("\\", "")

    if '-' in str(checked):
        if isinstance(checked, float):
            checked = str(checked).replace('.', ',')
        return f"***{regex_escaper(str(checked))}{profit.currency}*** {regex_escaper(comment)}"
    return regex_escaper(f"+{str(checked).replace('.', ',')}{profit.currency} от {profit.source_id.source}. {comment}")


def check_if_float(profit_summa):
    try:
        return int(profit_summa)
    except ValueError:
        return float(profit_summa)
