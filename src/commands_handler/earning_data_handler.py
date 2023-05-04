from buttons.buttons_all_icome_sources import buttons_all_income_sources
from commands_handler.base_data_expense_or_earnings_handler import base_data_handler
from cruds.source_of_income_cruds import source_of_income_cruds


def earnings_data_handler(message, loan):
    """
    Base earnings  handler
    :param message: chat message
    :param loan: current bot instance
    :return: None
    """
    all_sources = source_of_income_cruds.get_all_sources()
    buttons_all_income_sources(message, loan, all_sources)


def earnings_insert_data_handler(message, loan):
    """
    Uses if agent select source but NOT the other
    :param agent: current agent
    :param message: chat message
    :param loan: current bot instance
    :return:
    """
    base_data_handler(message, loan)


def earnings_with_other_source_insert_data_handler(message, loan):
    """
    Uses if agent select OTHER source
    :param message: chat message
    :param loan: current bot instance
    :return:
    """
    loan.send_message(message.chat.id, "Введите источник дохода")
    loan.register_next_step_handler(message, lambda msg: base_data_handler(msg, loan, True))
