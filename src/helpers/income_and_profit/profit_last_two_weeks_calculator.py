from datetime import datetime, timedelta
from typing import List

from cruds.source_of_income_cruds import source_of_income_cruds
from helpers.apis.get_currency_api import get_actual_currency
from helpers.enums.currency_enum import CurrencyEnum
from helpers.enums.inline_buttons_helper_enum import InlineButtonsHelperEnum
from models.admins import LoanAdminsModel
from models.earning_model import EarningsModel


def get_profit_of_last_two_weeks(agent: LoanAdminsModel):
    two_weeks_ago = datetime.utcnow() - timedelta(weeks=2)

    profit = source_of_income_cruds.get_source_percent_and_summa_by_username_last_two_weeks(agent.admin_username,
                                                                                            two_weeks_ago)
    return generate_profit_table(profit)


def generate_profit_table(profits: List[EarningsModel]):
    table = []
    earned = []
    if profits:
        uah, eur = get_actual_currency()

        for profit in profits:
            # get earned money
            if profit.source_id.source != InlineButtonsHelperEnum.OTHER:
                table.append(create_profit_string(profit))
                earned.append(get_all_summa_of_profit(profit, uah, eur))

        if eur and uah:
            earnings = f'***ОБЩАЯ СУММА {escape_reserved_chars(str(sum(earned)))}$***'
            return '{}'.format('\n'.join(
                table)) + f'\nТекущие курсы: {str(uah).replace(".", ",")} грн/долл и {str(eur).replace(".", ",")} долл/евро\n\n' + \
                   str(earnings).replace('.', ',')

        return "Произошла ошибка, попробуйте ещё раз"

    return 'Дохода за последние две недели пока нет'


def get_all_summa_of_profit(profit, uah, eur):
    earned = 0
    if str(profit.source_id.percent).strip():
        if profit.currency == CurrencyEnum.DOLLAR:
            earned += round(percent_calculator(percent=profit.source_id.percent, summa=profit.summa))

        elif profit.currency == CurrencyEnum.UAH:
            earned += round(percent_calculator(percent=profit.source_id.percent, summa=profit.summa)) / uah

        elif profit.currency == CurrencyEnum.EURO:

            earned += round(percent_calculator(percent=profit.source_id.percent, summa=profit.summa)) / eur

    return float(round(earned, 1))


def date_changer(date):
    dt_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    return dt_object.strftime('%d %b')


def escape_reserved_chars(summa):
    if float(summa):
        return str(summa).replace('-', '\\-')
    return summa


def percent_calculator(summa, percent):
    return (int(summa) * int(percent)) / 100


def create_profit_string(profit: EarningsModel):
    return f"{date_changer(str(profit.time_created))}" \
           f" {profit.source_id.source} " \
           f"{profit.source_id.percent}% от " \
           f"{profit.summa} {profit.currency} \\= " \
           f"{str(round(percent_calculator(percent=profit.source_id.percent, summa=profit.summa)))} {profit.currency}\n"
