from telebot import types

from helpers.income_and_profit.profit_last_two_weeks_calculator import get_profit_of_last_two_weeks


def buttons_get_previous_incomes(message, loan, agent):
    """
    Button to get prev incomes info
    :param message: chat message
    :param loan: current bot instance
    :return: None
    """
    loan.send_message(chat_id=message.chat.id, text=get_profit_of_last_two_weeks(agent), parse_mode='MarkdownV2')

    keyboard = types.InlineKeyboardMarkup()
    prev_incomes = types.InlineKeyboardButton(text='Ранее', callback_data='prev_incomes')
    keyboard.row(prev_incomes)

    loan.send_message(message.chat.id, 'Просмотрите более ранние транзакции', reply_markup=keyboard)
