from cruds.earning_cruds import earnings_cruds
from helpers.inform_message_creator.create_balance_message import create_balance_message
from models.admins import LoanAdminsModel


def get_agent_balance(message, loan, agent: LoanAdminsModel):
    """
    Calculate agent balance
    :param message: chat message
    :param loan: bot instance
    :param agent: current agent
    :return:
    """
    earnings = earnings_cruds.get_earning_by_agent_id(agent.id)

    loan.send_message(chat_id=message.chat.id, text=create_balance_message(agent.admin_username, earnings), parse_mode='MarkdownV2')
