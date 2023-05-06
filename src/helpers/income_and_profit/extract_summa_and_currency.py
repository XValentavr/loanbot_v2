import re

from helpers.enums.currency_enum import CurrencyEnum
from helpers.enums.error_enum import ErrorEnum


def extract_necessary_data(message):
    ready_to_extract = message.split(', верно?')[0]
    return extract_comment(ready_to_extract)


def extract_comment(message):
    """
    Get all data from string
    :param message: incame string to check
    :return: amount, currency and comment
    """
    match = re.search(r'(\d+)\s*(\S+)', message)

    if match:
        amount = match.group(1)
        currency = check_if_dollar(match.group(2))
        left_text = re.sub(r'(\d+)\s*(\S+)', '', message).strip()

        if currency == ErrorEnum.CURRENCY_NOT_FOUND:
            return '', '', ErrorEnum.CURRENCY_NOT_FOUND

        return amount, currency, left_text


def check_if_dollar(currency):
    dollars = ["дол", "$", "$.", "долл", "дол.", "долл.", "долларов.", "доллар", "долларов", "доллар.", 'usdt', 'usd']

    pattern = '|'.join([re.escape(d) for d in dollars])
    if bool(re.search(pattern, currency.lower())):
        return CurrencyEnum.DOLLAR

    return check_if_uah(currency)


def check_if_uah(currency):
    uah = ["uah", "грн", "грн.", "гривен", "гривен.", "гривень", "гривень.", "uah."]

    pattern = '|'.join([re.escape(u) for u in uah])
    if bool(re.search(pattern, currency.lower())):
        return CurrencyEnum.UAH

    return check_if_euro(currency)


def check_if_euro(currency):
    euros = ["eur", "euro", "eur.", "euro.", "евро", "евро.", "евр.", "евр", "євро.", "євро"]

    pattern = '|'.join([re.escape(e) for e in euros])
    if bool(re.search(pattern, currency.lower())):
        return CurrencyEnum.EURO

    return ErrorEnum.CURRENCY_NOT_FOUND
