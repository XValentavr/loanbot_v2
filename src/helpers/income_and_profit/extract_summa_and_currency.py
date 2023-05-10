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
    match = re.search(r'(\d+(?:\.\d+)?)\s+(\w+)', message)

    if match:
        amount = amount_checker(match.group(1))
        currency = check_if_dollar(match.group(2))
        comment = comment_slasher(extract_agent_comment(message, [amount, match.group(2)]))
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
    uah = ["uah", "грн", "грн.", "гривен", "гривен.", "гривень", "гривны",  "гривень.", "uah."]

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


def extract_agent_comment(string_to_clear, words_to_remove):
    for word in words_to_remove:
        string_to_clear = string_to_clear.replace(word, "")
    return string_to_clear.strip()


def amount_checker(amount):
    if ',' in amount:
        return amount.replace(',', '.')
    return amount


def comment_slasher(comment):
    return comment.replace('.', '\\.')
