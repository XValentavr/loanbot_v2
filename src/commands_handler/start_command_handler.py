from aiogram import types

from commands_handler.message_handler import echo_handler


async def start_command_handler(message: types.Message):
    from bot import loan

    await message.reply("Введіть пароль!")
    loan.register_message_handler(echo_handler)
