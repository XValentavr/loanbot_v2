import uuid
from datetime import timedelta

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
    def get_all_by_agent_id_and_time(agent: LoanAdminsModel, date_to_check) -> WithdrawModel:
        if date_to_check:
            interval_start = date_to_check[0].strftime("%Y-%m-%d")
            interval_end = (date_to_check[1] + timedelta(days=1)).strftime("%Y-%m-%d")

            return (
                session.query(WithdrawModel)
                .filter(WithdrawModel.agent_source_id == agent.id)
                .filter(WithdrawModel.time_created.between(interval_start, interval_end))
                .all()
            )
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
