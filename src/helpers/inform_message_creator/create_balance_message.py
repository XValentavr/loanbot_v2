from typing import List, Dict

from helpers.enums.currency_enum import CurrencyEnum
from models.earning_model import EarningsModel
from prettytable import PrettyTable


def create_balance_message(earnings):
    """
    Create pretty table to chat
    :param earnings: current agent earnings
    :return: changed string
    """
    table = PrettyTable(['Валюта', 'Баланс'])

    balances = create_balance(earnings)
    if balances:
        for currency, balance in balances.items():
            table.add_row([currency, balance])

        return '```{}```'.format(table) + '\n' + create_balance_history(earnings)
    return 'Баланса пока нет'


def dollar_calculator(earnings: List[EarningsModel]):
    return sum([int(earn.summa) for earn in earnings if earn.currency == CurrencyEnum.DOLLAR])


def eur_calculator(earnings: List[EarningsModel]):
    return sum([int(earn.summa) for earn in earnings if earn.currency == CurrencyEnum.EURO])


def uah_calculator(earnings: List[EarningsModel]):
    return sum([int(earn.summa) for earn in earnings if earn.currency == CurrencyEnum.UAH])


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

    if dollar != 0:
        balance['USD'] = dollar

    if eur != 0:
        balance['EUR'] = eur

    if uah != 0:
        balance['UAH'] = uah

    return balance


def create_balance_history(profits: List[EarningsModel]):
    history = []
    for number, profit in enumerate(profits):
        if number < 10:
            history.append(history_template(profit, number))

    return '\n'.join(history)


def history_template(profit: EarningsModel, number):
    from helpers.income_and_profit.profit_last_two_weeks_calculator import date_changer
    return f"{number + 1}\\.{date_changer(str(profit.time_created))}: {escaper(profit.summa)} {profit.currency}\\. Клиент \\- {profit.source_id.source}"


def escaper(string):
    if '-' in string:
        string = str(string).replace('-', '\\-')
        return f"выведено {string}"
    return f"внесено {string}"
