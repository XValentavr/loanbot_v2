import calendar
import re
from datetime import datetime
from typing import List

from cruds.source_of_income_cruds import source_of_income_cruds
from helpers.apis.get_currency_api import get_actual_currency
from helpers.enums.currency_enum import CurrencyEnum
from helpers.enums.inline_buttons_helper_enum import InlineButtonsHelperEnum
from helpers.helper_functions import regex_escaper, create_profit_template
from models.admins import LoanAdminsModel
from models.earning_model import EarningsModel


def get_profit_of_last_two_weeks(agent: LoanAdminsModel, for_withdrawal=False):
    first_part, second_part = create_proportional_parts_of_month()

    profit_for_first_part = source_of_income_cruds.get_source_percent_and_summa_by_username_last_two_weeks(
        agent.admin_username, first_part)
    # withdrawal_first = withdraw_cruds.get_all_by_agent_id_and_time(agent=agent, date_to_check=first_part)
    withdrawal_first = None
    first_month_part_result = generate_profit_table(profit_for_first_part, withdrawal_first, for_withdrawal)

    # get for second part of a month
    profit_for_second_part = source_of_income_cruds.get_source_percent_and_summa_by_username_last_two_weeks(
        agent.admin_username, second_part
    )

    # withdrawal_second = withdraw_cruds.get_all_by_agent_id_and_time(agent=agent, date_to_check=second_part)
    withdrawal_second = None

    second_month_part_result = generate_profit_table(profit_for_second_part, withdrawal_second, for_withdrawal)

    # generate result
    return generate_string_for_graded_month(first_month_part_result, second_month_part_result)


def generate_profit_table(
        profits: List[EarningsModel], withdrawal, for_withdrawal, is_for_main_agent=False,
        for_main_agent_withdrawal=False
):
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
                earned.append(get_all_summa_of_profit(profit))
        if eur and uah and (earned or is_for_main_agent):
            if withdrawal:
                withdrawal_to_string = [f'***{regex_escaper(include_withdrawal(withdraw))}***' for withdraw in
                                        withdrawal]
                withdrawal_summa = get_withdrawal_summa(withdrawal)
            earnings = create_profit_template(earned, withdrawal_summa,
                                              for_main_agent_withdrawal=for_main_agent_withdrawal)

            if is_for_main_agent or for_withdrawal:
                return earnings

            table_data = '\n'.join(table)
            return (
                    '{}'.format(table_data.replace(".", ","))
                    + '\n'.join(withdrawal_to_string)
                    + f'\n\nТекущие курсы: {str(uah).replace(".", ",")} грн/долл и'
                      f' {str(eur).replace(".", ",")} долл/евро\n\n' + earnings
            ).replace('=', '\\=')
        elif not eur or not uah:
            return "Произошла ошибка, попробуйте ещё раз"

    return 'Дохода за последние две недели пока нет'


def get_all_summa_of_profit(profit):
    earned = 0
    if str(profit.source_percent).strip():
        if profit.currency == CurrencyEnum.DOLLAR:
            earned += round(percent_calculator(percent=profit.source_percent, summa=profit.summa), 2)

        elif profit.currency == CurrencyEnum.UAH:
            earned += round(percent_calculator(percent=profit.source_percent, summa=profit.summa), 2) / float(profit.uah)

        elif profit.currency == CurrencyEnum.EURO:
            earned += round(percent_calculator(percent=profit.source_percent, summa=profit.summa), 2) / float(profit.eur)

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
    comment = profit.comment.replace("\\", "")

    if not for_main_admin:
        return (
            f"{date_changer(str(profit.time_created))}"
            f" {profit.source_id.source} "
            f"{profit.source_percent}% от "
            f"{profit.summa} {profit.currency} = "
            f"{str(round(percent_calculator(percent=profit.source_percent, summa=profit.summa), 2))} {profit.currency}\n"
        )

    return (
            regex_escaper(
                f"{date_changer(str(profit.time_created))}"
                f" {profit.source_id.source if float(profit.summa) > 0 else ''} "
                f"{profit.source_percent + ' % от ' if float(profit.summa) > 0 else ''}"
            )
            + f"***{escape_reserved_chars(str(profit.summa)).replace('.', ',')}*** {profit.currency}\\. {regex_escaper(comment)}"
    )


def include_withdrawal(withdrawal):
    return f'\n{date_changer(str(withdrawal.time_created))}' f' Выведено: ' f'{withdrawal.summa} $'


def get_withdrawal_summa(withdrawal):
    return sum([int(withdraw.summa) for withdraw in withdrawal])


def create_proportional_parts_of_month(month=None):
    from datetime import date, timedelta

    if not month:
        today = date.today()
        current_month = today.month
        current_year = today.year
    else:
        current_month = list(calendar.month_name).index(month.get('month').capitalize()) + 1
        current_year = month.get('year')
    if current_month == 12:
        next_month = 1
        next_year = current_year + 1
    else:
        next_month = current_month + 1
        next_year = current_year

    days_in_month = date(next_year, next_month, 1) - date(current_year, current_month, 1)
    interval_start_first = date(current_year, current_month, 1)
    interval_end_first = date(current_year, current_month, int(days_in_month.days / 2))

    interval_start_second = interval_end_first + timedelta(days=1)
    interval_end_second = date(current_year, current_month, days_in_month.days)

    return [interval_start_first, interval_end_first], [interval_start_second, interval_end_second]


def generate_string_for_graded_month(first_part, second_part, for_main_agent=False, months=None):
    part_1, part_2 = create_proportional_parts_of_month(month=months)
    first_part_string = second_part_string = ''
    if 'пока нет' not in first_part and first_part:
        first_part_string = f'``` {part_1[0].strftime("%d %B")}\\-{part_1[1].strftime("%d %B")}``` \n\n' f'{first_part}'
    if 'пока нет' not in second_part and second_part:
        second_part_string = f'\n\n``` {part_2[0].strftime("%d %B")}\\-{part_2[1].strftime("%d %B")}``` \n\n' f'{second_part}'

    complex_string = first_part_string + second_part_string
    if for_main_agent:
        return complex_string
    return complex_string + get_general_summa_per_month(first_part, second_part)


def get_general_summa_per_month(first_part, second_part):
    first_summa = re.findall(r'(\-?\d+\\,\d+)\$', first_part)[-1] if 'пока нет' not in first_part else 0
    second_summa = re.findall(r'(\-?\d+\\,\d+)\$', second_part)[-1] if 'пока нет' not in second_part else 0

    final_summa = float(str(first_summa).replace(",", ".").replace("\\", "")) + float(
        str(second_summa).replace(",", ".").replace("\\", ""))
    return f'\n\n``` СУММА ЗА МЕСЯЦ {round(final_summa, 2)}$```'.replace('.', ',')
