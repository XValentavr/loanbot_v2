from datetime import datetime, timedelta
from typing import List

from prettytable import PrettyTable

from cruds.source_of_income_cruds import source_of_income_cruds
from helpers.apis.get_currency_api import get_actual_currency
from helpers.enums.currency_enum import CurrencyEnum
from models.admins import LoanAdminsModel
from models.earning_model import EarningsModel


def get_profit_of_last_two_weeks(agent: LoanAdminsModel):
    two_weeks_ago = datetime.utcnow() - timedelta(weeks=2)

    profit = source_of_income_cruds.get_source_percent_and_summa_by_username_last_two_weeks(agent.admin_username,
                                                                                            two_weeks_ago)
    return generate_profit_table(profit)


def generate_profit_table(profits: List[EarningsModel]):
    table = PrettyTable(['Дата', 'Источник', 'Сумма'])
    earned = []
    if profits:
        uah, eur = get_actual_currency()

        for profit in profits:
            # get earned money

            table.add_row([date_changer(str(profit.time_created)), profit.source_id.source,
                           f'{profit.summa} {profit.currency}'])

            earned.append(get_all_summa_of_profit(profit, uah, eur))

        if eur and uah:
            earnings = f'***ОБЩАЯ СУММА {sum(earned)}***'
            return '```{}```'.format(
                table) + f'\nТекущие курсы: {str(uah).replace(".", ",")} грн/долл и {str(eur).replace(".", ",")} долл/евро\n\n' + \
                   str(earnings).replace('.', ',')

        return "Произошла ошибка, попробуйте ещё раз"

    return 'Дохода за последние две недели пока нет'


def get_all_summa_of_profit(profit, uah, eur):
    earned = 0

    if profit.currency == CurrencyEnum.DOLLAR:
        if str(profit.source_id.percent).strip():
            earned += round(int(profit.summa) / int(profit.source_id.percent))
        else:
            earned += round(int(profit.summa))

    elif profit.currency == CurrencyEnum.UAH:
        if str(profit.source_id.percent).strip():
            earned += round(int(profit.summa) / int(profit.source_id.percent)) / uah
        else:
            earned += round(int(profit.summa))

    elif profit.currency == CurrencyEnum.EURO:
        if str(profit.source_id.percent).strip():

            earned += round(int(profit.summa) / int(profit.source_id.percent)) / eur
        else:
            earned += round(int(profit.summa))

    return float(round(earned, 1))


def date_changer(date):
    dt_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    return dt_object.strftime('%d %b')
