from aiogram import types

from cruds.agent_cruds import agent_cruds
from helpers.encrypt_and_decrypt import encryptor


async def echo_handler(message: types.Message):
    from bot import loan

    password = message.text
    agent_username = message.from_user.username

    agents = agent_cruds.get_all_agents()
    for agent in agents:
        if encryptor.compare_password(agent.admin_password, password) and agent.admin_username == agent_username:
            agent_cruds.update_agent_is_logged_in(agent)

            await message.answer(f"Вы успешно вошли в аккаунт")
            loan.message_handlers.unregister(echo_handler)
            break

        await message.answer(f"Пароль неверен. Повторите попытку")
        break

