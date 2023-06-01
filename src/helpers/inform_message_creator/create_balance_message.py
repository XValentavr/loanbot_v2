import re
from typing import List, Dict

from helpers.enums.currency_enum import CurrencyEnum
from helpers.helper_functions import regex_escaper
from models.earning_model import EarningsModel
from prettytable import PrettyTable


def create_balance_message(earnings, include_history=True):
    """
    Create pretty table to chat
    :param earnings: current agent earnings
    :param include_history: s
    :return: changed string
    """
    table = PrettyTable(['Валюта', 'Баланс'])
    balances = create_balance(earnings)
    history = create_balance_history(earnings)
    if balances or history:
        for currency, balance in balances.items():
            table.add_row([currency, balance])
        if include_history:
            return '```{}```'.format(table) + '\n' + history
        return '```{}```'.format(table)
    return 'Баланса пока нет'


def dollar_calculator(earnings: List[EarningsModel]):
    return str(round(sum([float(earn.summa) for earn in earnings if earn.currency == CurrencyEnum.DOLLAR]), 2)).replace(
        '.', ',')


def eur_calculator(earnings: List[EarningsModel]):
    return str(round(sum([float(earn.summa) for earn in earnings if earn.currency == CurrencyEnum.EURO]), 6)).replace(
        '.', ',')


def uah_calculator(earnings: List[EarningsModel]):
    return str(round(sum([float(earn.summa) for earn in earnings if earn.currency == CurrencyEnum.UAH]), 2)).replace(
        '.', ',')


def create_balance(earnings) -> Dict:
    """
    Create dict of currency and balance
    :param earnings: agent earnings
    :return: dict of currency and balance
    """
    balance = {}

    dollar = dollar_calculator(earnings)
    eur = eur_calculator(earnings)
    uah = uah_calculator(earnings)

    balance['USD'] = dollar

    balance['EUR'] = eur

    balance['UAH'] = uah

    return balance


def create_balance_history(profits: List[EarningsModel]):
    history = []
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
    return regex_escaper(
        f"+{str(checked).replace('.', ',')}{profit.currency} от {profit.source_id.source}. {comment}")


def check_if_float(profit_summa):
    try:
        return int(profit_summa)
    except ValueError:
        return float(profit_summa)
