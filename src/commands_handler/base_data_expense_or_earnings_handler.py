from typing import Dict

from buttons.button_ready_or_not import buttons_ready_or_not
from buttons.buttons_back import buttons_back
from buttons.buttons_if_logged_in import buttons_if_logged_in
from cruds.earning_cruds import earnings_cruds
from cruds.source_of_income_cruds import source_of_income_cruds
from helpers.enums.error_enum import ErrorEnum
from helpers.enums.inline_buttons_helper_enum import InlineButtonsHelperEnum
from helpers.income_and_profit.extract_summa_and_currency import extract_necessary_data
from helpers.inform_message_creator.create_balance_message import check_if_float
from send_to_owner.send_message_to_owner import send_message_to_owner

other_source: Dict = {}


def base_data_handler(message, loan, income_source=None):
    """
    Base command handler for expenses and earnings and have the same logic
    :param message: current message
    :param loan: current bot instance
    :param income_source: if transactions is income
    :return: None
    """
    if income_source:
        other_source[message.from_user.username] = message.text

    loan.send_message(message.chat.id, "Внесите сумму и комментарий")
    loan.register_next_step_handler(message, lambda msg: check_summa_and_comment(msg, loan))


def check_summa_and_comment(message, loan):
    """
    Check if all is ok and ready
    :param message: message of chat
    :param loan: bot instance
    :return: None
    """
    buttons_ready_or_not(message, loan)


def ready_event(message, agent, loan, source, expense, call_count):
    """
    Function to handle transaction
    :param message: current message
    :param agent: current agent user
    :param loan: but state
    :param source: source of income or expense
    :param expense: if transaction is expense
    :return: None
    """
    try:
        amount, currency, text = extract_necessary_data(message.text)
        call_count = call_count and call_count.get('call')
        if call_count is not None and call_count == 0:
            if text == ErrorEnum.CURRENCY_NOT_FOUND:
                loan.send_message(message.chat.id, ErrorEnum.CURRENCY_NOT_FOUND, reply_to_message_id=message.id)
                base_data_handler(message, loan)
            else:
                earning = earnings_cruds.insert_source(
                    summa=check_type_of_transaction_and_revert_amount(expense, amount),
                    comment=text.split('верно?')[0].strip(),
                    source_id=source.id
                    if not other_source.get(agent.admin_username) and not expense
                    else source_of_income_cruds.get_source_by_source_name(InlineButtonsHelperEnum.OTHER).id,
                    agent_id=agent.id,
                    currency=currency,
                    is_other_source=other_source.get(agent.admin_username) if other_source.get(agent.admin_username) and not expense else None,
                )

                loan.send_message(message.chat.id, "Транзакция успешная!")
                send_message_to_owner(loan, earning, agent.admin_username)
                if other_source.get(agent.admin_username):
                    del other_source[agent.admin_username]

                buttons_if_logged_in(message, loan)
    except Exception:
        loan.send_message(
            message.chat.id, "Что-то пошло не так, попробуйте ещё раз", reply_to_message_id=message.id, reply_markup=buttons_back()
        )


def change_event(message, loan):
    base_data_handler(message, loan)


def check_type_of_transaction_and_revert_amount(expense, amount):
    """
    if outcome that revert int
    :param expense: if is expense transaction
    :param amount: amount of transaction
    :return: reverted amount
    """
    if expense:
        return str(check_if_float(amount) * -1)
    return amount
