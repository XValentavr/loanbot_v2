import uuid

from create_engine import session
from models.admins import LoanAdminsModel
from models.earning_model import EarningsModel
from models.withdraw_model import WithdrawModel


class WithdrawalCruds:
    @staticmethod
    def insert_agent(summa: str, agent: LoanAdminsModel) -> WithdrawModel:
        withdraw = WithdrawModel(summa=summa, agent_source_id=agent.id)

        withdraw.id = uuid.uuid4()

        session.add(withdraw)
        session.commit()

    @staticmethod
    def get_all_by_agent_id(agent: LoanAdminsModel) -> WithdrawModel:
        return (
            session.query(WithdrawModel)
            .filter(WithdrawModel.agent_source_id == agent.id)
            .all()
        )

    @staticmethod
    def get_all_by_agent_username(agent: LoanAdminsModel) -> WithdrawModel:
        return (
            session.query(WithdrawModel)
            .join(EarningsModel.agent_id)
            .join(EarningsModel.source_id)
            .filter(LoanAdminsModel.admin_username == agent.admin_username)
            .all()
        )


withdraw_cruds = WithdrawalCruds()
