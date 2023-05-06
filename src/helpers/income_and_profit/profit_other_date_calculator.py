import calendar

from datetime import datetime, timedelta

from cruds.source_of_income_cruds import source_of_income_cruds
from helpers.apis.get_currency_api import get_actual_currency
from helpers.enums.currency_enum import CurrencyEnum
from models.admins import LoanAdminsModel


def get_profit_of_other_dates(agent: LoanAdminsModel):
    other_date = datetime.utcnow() - timedelta(weeks=2)
    profits = source_of_income_cruds.get_source_percent_and_summa_by_username_other_date(agent.admin_username,
                                                                                         other_date)
    return create_table_for_other_profits(profits)


def create_table_for_other_profits(profits):
    profits_by_month_list = []
    if profits:
        uah, eur = get_actual_currency()
        # combine profit by summa and date
        for profit in profits:
            profits_by_month_list.append(calculate_month_profit(*profit, uah=uah, eur=eur))

        # create string of month profits
        pretty_string = ''
        if profits_by_month_list:
            for combines in combine_by_month(profits_by_month_list):
                pretty_string = pretty_string + f'```{combines.get("month")}```\n```{combines.get("summa")}{CurrencyEnum.DOLLAR}```'
            return pretty_string

        return "Произошла ошибка, попробуйте ещё раз"

    return 'Дохода пока нет'


def calculate_month_profit(month, year, currency, summa, uah, eur):
    profit_dict = {'summa': 0, 'month': f'{calendar.month_name[month]}-{year}'}
    if uah and eur:
        if currency == CurrencyEnum.DOLLAR:
            profit_dict['summa'] = summa

        elif currency == CurrencyEnum.UAH:
            profit_dict['summa'] = round(profit_dict.get('summa') + int(summa) / uah)

        elif currency == CurrencyEnum.EURO:
            profit_dict['summa'] = round(profit_dict.get('summa') + int(summa) / eur)

        return profit_dict
    return {}


def combine_by_month(data_dict):
    combined_data = {}
    for item in data_dict:
        month = item['month']
        summa = item['summa']
        if month not in combined_data:
            combined_data[month] = {'summa': summa, 'month': month}
        else:
            combined_data[month]['summa'] += summa

    return list(combined_data.values())
