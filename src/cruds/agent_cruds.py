import uuid

from create_engine import session
from models.admins import LoanAdminsModel


class AgentCruds:
    @staticmethod
    def insert_agent(username: str, password: str, is_logged_in: bool):
        admins = LoanAdminsModel(admin_username=username, admin_password=password, is_login=is_logged_in)

        admins.id = uuid.uuid4()

        session.add(admins)
        session.commit()

    @staticmethod
    def get_all_agents():
        return (
            session.query(LoanAdminsModel).all()
        )

    @staticmethod
    def get_agents_to_check_balance(agent):
        return (
            session.query(LoanAdminsModel)
            .filter(LoanAdminsModel.admin_username != agent.admin_username)
            .all()
        )

    @staticmethod
    def update_agent_is_logged_in(agent: LoanAdminsModel):
        agent.is_login = not agent.is_login

        session.commit()

    @staticmethod
    def get_by_username(username: str) -> LoanAdminsModel:
        return (
            session.query(LoanAdminsModel)
            .filter(LoanAdminsModel.admin_username == username)
            .first()
        )


agent_cruds = AgentCruds()
