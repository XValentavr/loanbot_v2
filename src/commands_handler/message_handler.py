from cruds.agent_cruds import agent_cruds
from helpers.encrypt_and_decrypt import encryptor


def start_handler(message, loan):
    """
    Check user and his password
    :param message: current message of chat
    :param loan: current bot instance
    :return: None
    """
    password = message.text
    agent_username = message.from_user.username

    agents = agent_cruds.get_all_agents()
    for agent in agents:
        if encryptor.compare_password(agent.admin_password, password) and agent.admin_username == agent_username:
            agent_cruds.update_agent_is_logged_in(agent)

            loan.send_message(message.chat.id, "Вы успешно вошли в аккаунт")
            return True

        loan.send_message(message.chat.id, "Пароль неверен. Повторите попытку /start")
        return False
