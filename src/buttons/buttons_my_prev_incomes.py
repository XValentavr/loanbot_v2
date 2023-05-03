from telebot import types


def buttons_get_previous_incomes(message, loan):
    """
    Button to get prev incomes info
    :param message: chat message
    :param loan: current bot instance
    :return: None
    """
    keyboard = types.InlineKeyboardMarkup()
    prev_incomes = types.InlineKeyboardButton(text='button1', callback_data='prev_incomes')
    keyboard.row(prev_incomes)

    loan.send_message(message.chat.id, 'Choose a button:', reply_markup=keyboard)
