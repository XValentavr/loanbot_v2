import telebot

bot_token = '5858596575:AAHdOwlJ8k_Kar7bp9pbXivIx8OS3ipYlbc'
bot = telebot.TeleBot(bot_token)


def get_user_id(username):
    try:
        chat = bot.get_chat(username)
        return chat.id
    except telebot.apihelper.ApiException:
        return None


# Usage example
username = 'Valentavr'
user_id = get_user_id(username)

if user_id:
    print(f"The user ID for {username} is {user_id}")
else:
    print(f"User {username} not found.")
