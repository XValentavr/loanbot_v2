from commands_handler.message_handler import start_handler


def check_password_and_set_privacy(message, loan):
    """
    Check password in login process
    :param message: current chat message
    :param loan: bot instance
    :return: None
    """
    start_handler(message, loan)
