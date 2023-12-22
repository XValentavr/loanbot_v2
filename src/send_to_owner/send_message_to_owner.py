from helpers.creds import Creds
from models.earning_model import EarningsModel


def generate_message_for_owner(instance: EarningsModel, admin: str):
    summa = instance.summa
    if '-' not in summa:
        return f'{admin} внес доход {instance.summa}{instance.currency}\nКлиент - {instance.source_name}\n{instance.comment}\\. Курс USD/UAH: {instance.uah}'.replace(
            '\\', ''
        )
    return f'{admin} внес расход {instance.summa}{instance.currency}\n{instance.comment}\\. Курс USD/UAH: {instance.uah}'.replace('\\', '')


def generate_withdraw_message_for_owner(summa: str, admin: str):
    return f'{admin} запросил вывод {summa}$'.replace('\\', '')


def send_message_to_owner(loan, instance: EarningsModel, admin: str, withdraw=None):
    if withdraw:
        loan.send_message(Creds.OWNER_USER_ID, generate_withdraw_message_for_owner(withdraw, admin))
    else:
        loan.send_message(Creds.OWNER_USER_ID, generate_message_for_owner(instance, admin))
