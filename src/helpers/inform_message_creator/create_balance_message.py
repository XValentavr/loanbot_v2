from typing import List, Dict

from helpers.enums.currency_enum import CurrencyEnum
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
    return str(sum([float(earn.summa) for earn in earnings if earn.currency == CurrencyEnum.DOLLAR])).replace('.', ',')


def eur_calculator(earnings: List[EarningsModel]):
    return str(sum([float(earn.summa) for earn in earnings if earn.currency == CurrencyEnum.EURO])).replace('.', ',')


def uah_calculator(earnings: List[EarningsModel]):
    return str(sum([float(earn.summa) for earn in earnings if earn.currency == CurrencyEnum.UAH])).replace('.', ',')


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
    return f"{number + 1}\\. {date_changer(str(profit.time_created))}: {escaper(profit)} "


def escaper(profit):
    if '-' in profit.summa:
        string = str(profit.summa).replace('-', '\\-')
        string = string.replace('.', ',')
        return f"***{string}{profit.currency}*** {profit.comment}"
    return f"\\+{str(profit.summa).replace('.', ',')}{profit.currency} от {profit.source_id.source}"
