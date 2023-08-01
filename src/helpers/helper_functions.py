import re


def regex_escaper(string):
    string =  re.escape(string)
    string = string.replace('=', '\\=')
    return string


def remove_all_chars(withdrawal: str):
    return re.sub("[^0-9]", "", withdrawal.split()[0])


def create_profit_template(earned, withdrawal_summa, for_main_agent_withdrawal):
    from helpers.income_and_profit.profit_last_two_weeks_calculator import escape_reserved_chars

    if not for_main_agent_withdrawal:
        return f'***ОБЩАЯ СУММА ЗА ПЕРИОД {regex_escaper(str(round(float(escape_reserved_chars(str(sum(earned)))) - withdrawal_summa, 2)))}$***'.replace(
            '.', ','
        )
    else:
        return regex_escaper(str(round(float(escape_reserved_chars(str(sum(earned)))), 2)))
