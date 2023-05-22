import re

from helpers.enums.currency_enum import CurrencyEnum
from helpers.enums.error_enum import ErrorEnum
from helpers.helper_functions import regex_escaper


def extract_necessary_data(message):
    ready_to_extract = message.split(', верно?')[0]
    return extract_comment(ready_to_extract)


def extract_comment(message):
    """
    Get all data from string
    :param message: incame string to check
    :return: amount, currency and comment
    """
    match = re.match(r'(?P<summa>[0-9,.]+)\s*(?P<currency>[a-zA-Zа-яА-Я$€]+)\s*(?P<comment>.*)', message)
    if match:
        amount = amount_checker(match.group('summa'))
        currency = check_if_dollar(match.group('currency'))
        comment = regex_escaper(match.group("comment"))
        if currency == ErrorEnum.CURRENCY_NOT_FOUND:
            return '', '', ErrorEnum.CURRENCY_NOT_FOUND

        return amount, currency, comment


def check_if_dollar(currency):
    dollars = ["дол", "$", "$.", "долл", "дол.", "долл.", "долларов.", "доллар", "долар", "доларов", "долларов",
               "доллар.", 'usdt', 'usd']

    pattern = '|'.join([re.escape(d) for d in dollars])
    if bool(re.search(pattern, currency.lower())):
        return CurrencyEnum.DOLLAR

    return check_if_uah(currency)


def check_if_uah(currency):
    uah = ["uah", "грн", "грн.", "гривен", "гривен.", "гривень", "гривны", "гривень.", "uah.", "UAH", "UAH."]

    pattern = '|'.join([re.escape(u) for u in uah])
    if bool(re.search(pattern, currency.lower())):
        return CurrencyEnum.UAH

    return check_if_euro(currency)


def check_if_euro(currency):
    euros = ["eur", "EUR", "EUR.", "€", "euro", "eur.", "euro.", "евро", "евро.", "евр.", "евр", "євро.", "євро"]

    pattern = '|'.join([re.escape(e) for e in euros])
    if bool(re.search(pattern, currency.lower())):
        return CurrencyEnum.EURO

    return ErrorEnum.CURRENCY_NOT_FOUND



def amount_checker(amount):
    if ',' in amount:
        return amount.replace(',', '.')
    return amount
