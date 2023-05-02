import uuid

from create_engine import session
from models.admins import LoanAdmins


class AgentCruds:
    @staticmethod
    def insert_agent_cruds(username: str, password: str, is_logged_in: bool):
        admins = LoanAdmins(admin_username=username, admin_password=password, is_login=is_logged_in)

        admins.id = uuid.uuid4()

        session.add(admins)
        session.commit()

    @staticmethod
    def get_all_agents():
        return (
            session.query(LoanAdmins).all()
        )

    @staticmethod
    def update_agent_is_logged_in(agent: LoanAdmins):
        agent.is_login = not agent.is_login

        session.commit()


agent_cruds = AgentCruds()
