from aiogram import Bot, Dispatcher, types

from commands_handler.start_command_handler import start_command_handler
from helpers.creds import Creds


class CreateBot:
    @staticmethod
    def create_bot():
        bot = Bot(token=Creds.LOAN_BOT_ID)
        return Dispatcher(bot)


loan = CreateBot().create_bot()


@loan.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await start_command_handler(message)
