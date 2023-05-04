from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from helpers.enums.inline_buttons_helper_enum import InlineButtonsHelperEnum


def buttons_ready_or_not(message, loan):
    """
    Create button to check if transaction is ready
    :param message:  message of chat
    :param loan: current bot instance
    :return: None
    """
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton('Подтвердить', callback_data=InlineButtonsHelperEnum.READY),
        InlineKeyboardButton('Изменить', callback_data=InlineButtonsHelperEnum.CHANGE)
    )

    loan.send_message(message.chat.id, generate_reply_message(message),
                      reply_to_message_id=message.message_id,
                      reply_markup=markup)


def generate_reply_message(message):
    return f'{message.text}, верно?'
