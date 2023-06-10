import calendar

from datetime import date

from cruds.source_of_income_cruds import source_of_income_cruds
from cruds.withdrawal_cruds import withdraw_cruds
from helpers.apis.get_currency_api import get_actual_currency
from helpers.enums.currency_enum import CurrencyEnum
from helpers.income_and_profit.profit_last_two_weeks_calculator import generate_profit_table
from models.admins import LoanAdminsModel


def get_profit_of_other_dates(agent: LoanAdminsModel, calculate_date=True, partial=None):
    if calculate_date:
        today = date.today()
        first_day_of_current_month = date(today.year, today.month, 1)

        all_profit = source_of_income_cruds.get_source_percent_and_summa_by_username_other_date(agent.admin_username,
                                                                                                first_day_of_current_month)
        return create_table_for_other_profits(all_profit)
    else:
        # withdrawal = withdraw_cruds.get_all_by_agent_id_and_time(agent=agent, date_to_check=partial)
        profit = source_of_income_cruds.get_source_percent_and_summa_by_username_last_two_weeks(
            agent.admin_username, partial)
        return generate_profit_table(profit, is_for_main_agent=True, for_withdrawal=False,
                                     withdrawal=None)


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
                pretty_string = pretty_string + f'```{combines.get("month")}```\n```{round(combines.get("summa"),2)}{CurrencyEnum.DOLLAR}```'
            return pretty_string

        return "Произошла ошибка, попробуйте ещё раз"

    return 'Дохода пока нет'


def calculate_month_profit(month, year, currency, summa, uah, eur):
    profit_dict = {'summa': 0, 'month': f'{calendar.month_name[month]}-{year}'}
    if uah and eur:
        if currency == CurrencyEnum.DOLLAR:
            profit_dict['summa'] = summa

        elif currency == CurrencyEnum.UAH:
            profit_dict['summa'] = round(profit_dict.get('summa') + int(summa) / uah, 2)

        elif currency == CurrencyEnum.EURO:
            profit_dict['summa'] = round(profit_dict.get('summa') + int(summa) / eur, 2)

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
