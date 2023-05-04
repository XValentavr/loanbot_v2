from commands_handler.base_data_expense_or_earnings_handler import base_data_handler


def expense_data_handler(message, loan):
    """
    handle expense button
    :param message: message of chat
    :param loan: current bot instance
    :return: None
    """
    base_data_handler(message, loan)
