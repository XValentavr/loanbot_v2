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


def generate_profit_table(profits: List[EarningsModel], is_for_main_agent=False):
    table = []
    earned = []
    if profits:
        uah, eur = get_actual_currency()

        for profit in profits:
            # get earned money
            if profit.source_id.source != InlineButtonsHelperEnum.OTHER:
                table.append(create_profit_string(profit))
                earned.append(get_all_summa_of_profit(profit, uah, eur))

        if eur and uah and earned:
            earnings = f'***ОБЩАЯ СУММА {round(float(escape_reserved_chars(str(sum(earned)))), 2)}$***'.replace('.',
                                                                                                                ',')

            if is_for_main_agent:
                return earnings

            table_data = '\n'.join(table)
            return '{}'.format(table_data.replace(".", ",")) + \
                   f'\nТекущие курсы: {str(uah).replace(".", ",")} грн/долл и' \
                   f' {str(eur).replace(".", ",")} долл/евро\n\n' + \
                   earnings
        elif not eur or not uah:
            return "Произошла ошибка, попробуйте ещё раз"

    return 'Дохода за последние две недели пока нет'


def get_all_summa_of_profit(profit, uah, eur):
    earned = 0
    if str(profit.source_id.percent).strip():
        if profit.currency == CurrencyEnum.DOLLAR:
            earned += round(percent_calculator(percent=profit.source_id.percent, summa=profit.summa), 2)

        elif profit.currency == CurrencyEnum.UAH:
            earned += round(percent_calculator(percent=profit.source_id.percent, summa=profit.summa), 2) / uah

        elif profit.currency == CurrencyEnum.EURO:

            earned += round(percent_calculator(percent=profit.source_id.percent, summa=profit.summa), 2) / eur

    return float(round(earned, 2))


def date_changer(date):
    dt_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    return dt_object.strftime('%d %b')


def escape_reserved_chars(summa):
    if float(summa):
        return str(summa).replace('-', '\\-')
    return summa


def percent_calculator(summa, percent):
    return (float(summa) * float(percent)) / 100


def create_profit_string(profit: EarningsModel, for_main_admin=False):
    if not for_main_admin:
        return f"{date_changer(str(profit.time_created))}" \
               f" {profit.source_id.source} " \
               f"{profit.source_id.percent}% от " \
               f"{profit.summa} {profit.currency} \\= " \
               f"{str(round(percent_calculator(percent=profit.source_id.percent, summa=profit.summa), 2))} {profit.currency}\n"

    return f"{date_changer(str(profit.time_created))}" \
           f" {profit.source_id.source if float(profit.summa) > 0 else ''} " \
           f"{profit.source_id.percent + ' % от ' if float(profit.summa) > 0 else ''}" \
           f"***{escape_reserved_chars(str(profit.summa)).replace('.', ',')}*** {profit.currency}"
