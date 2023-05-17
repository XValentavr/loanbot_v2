from datetime import datetime, timedelta
from typing import List

from cruds.source_of_income_cruds import source_of_income_cruds
from cruds.withdrawal_cruds import withdraw_cruds
from helpers.apis.get_currency_api import get_actual_currency
from helpers.enums.currency_enum import CurrencyEnum
from helpers.enums.inline_buttons_helper_enum import InlineButtonsHelperEnum
from helpers.helper_functions import regex_escaper, create_profit_template
from models.admins import LoanAdminsModel
from models.earning_model import EarningsModel


def get_profit_of_last_two_weeks(agent: LoanAdminsModel, for_withdrawal=False):
    two_weeks_ago = datetime.utcnow() - timedelta(weeks=2)

    profit = source_of_income_cruds.get_source_percent_and_summa_by_username_last_two_weeks(agent.admin_username,
                                                                                            two_weeks_ago)
    withdrawal = withdraw_cruds.get_all_by_agent_id(agent=agent)

    return generate_profit_table(profit, withdrawal, for_withdrawal)


def generate_profit_table(profits: List[EarningsModel],
                          withdrawal,
                          for_withdrawal,
                          is_for_main_agent=False,
                          for_main_agent_withdrawal=False):
    table = []
    earned = []
    withdrawal_to_string = []
    withdrawal_summa = 0
    if profits:
        uah, eur = get_actual_currency()

        for profit in profits:
            # get earned money
            if profit.source_id.source != InlineButtonsHelperEnum.OTHER:
                table.append(regex_escaper(create_profit_string(profit)).replace('=', '\\='))
                earned.append(get_all_summa_of_profit(profit, uah, eur))

        if eur and uah and earned:
            if withdrawal:
                withdrawal_to_string = [f'***{regex_escaper(include_withdrawal(withdraw))}***' for withdraw in
                                        withdrawal]
                withdrawal_summa = get_withdrawal_summa(withdrawal)
            earnings = create_profit_template(earned, withdrawal_summa, for_main_agent_withdrawal= for_main_agent_withdrawal)

            if is_for_main_agent or for_withdrawal:
                return earnings

            table_data = '\n'.join(table)
            return '{}'.format(table_data.replace(".", ",")) + \
                   '\n'.join(withdrawal_to_string) + \
                   f'\n\nТекущие курсы: {str(uah).replace(".", ",")} грн/долл и' \
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
               f"{profit.summa} {profit.currency} = " \
               f"{str(round(percent_calculator(percent=profit.source_id.percent, summa=profit.summa), 2))} {profit.currency}\n"

    return regex_escaper(f"{date_changer(str(profit.time_created))}"
                         f" {profit.source_id.source if float(profit.summa) > 0 else ''} "
                         f"{profit.source_id.percent + ' % от ' if float(profit.summa) > 0 else ''}") \
           + f"***{escape_reserved_chars(str(profit.summa)).replace('.', ',')}*** {profit.currency}"


def include_withdrawal(withdrawal):
    return f'\n{date_changer(str(withdrawal.time_created))}' \
           f' Выведено: ' \
           f'{withdrawal.summa} $'


def get_withdrawal_summa(withdrawal):
    return sum([int(withdraw.summa) for withdraw in withdrawal])
