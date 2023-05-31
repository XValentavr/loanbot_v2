from helpers.creds import Creds
from models.earning_model import EarningsModel


def generate_message_for_owner(instance: EarningsModel, admin: str):
    summa = instance.summa
    if '-' not in summa:
        return f'{admin} внес доход {instance.summa}{instance.currency}\nКлиент - {instance.source_name}\n{instance.comment}'.replace(
            '\\', '')
    return f'{admin} внес расход {instance.summa}{instance.currency}\n{instance.comment}'.replace('\\', '')


def send_message_to_owner(loan, instance: EarningsModel, admin: str):
    loan.send_message(Creds.OWNER_USER_ID, generate_message_for_owner(instance, admin))
