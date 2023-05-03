from typing import List

from telebot import types

from models.sources_of_income_model import SourcesOfIncomeModel


def buttons_all_income_sources(message, loan, sources: List[SourcesOfIncomeModel]):
    """
    Create buttons fore agent with income sources
    :param message: message of chat
    :param loan: current bot instance
    :param sources: all possible sources
    :return: None
    """
    source_sorted = sorted([source.source for source in sources])

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    for source in source_sorted:
        key = types.InlineKeyboardButton(text=source, callback_data=source)
        keyboard.add(key)

    loan.send_message(chat_id=message.chat.id, text="Источник", reply_markup=keyboard)
