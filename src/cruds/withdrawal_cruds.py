import uuid
from datetime import timedelta

from sqlalchemy import asc

from create_engine import session
from models.admins import LoanAdminsModel
from models.earning_model import EarningsModel
from models.withdraw_model import WithdrawModel


class WithdrawalCruds:
    @staticmethod
    def insert_agent(summa: str, agent: LoanAdminsModel) -> WithdrawModel:
        withdraw = WithdrawModel(summa=summa, agent_source_id=agent.id, admin_char=agent.admin_username)

        withdraw.id = uuid.uuid4()

        session.add(withdraw)
        session.commit()

    def get_all_by_agent_id_and_time(self, agent: LoanAdminsModel, date_to_check, current_month=None) -> WithdrawModel:
        if date_to_check:
            interval_start = date_to_check[0].strftime("%Y-%m-%d")
            interval_end = (date_to_check[1] + timedelta(days=1)).strftime("%Y-%m-%d")

            return (
                session.query(WithdrawModel)
                .order_by(asc(WithdrawModel.time_created))
                .filter(WithdrawModel.agent_source_id == agent.id)
                .filter(WithdrawModel.time_created.between(interval_start, interval_end))
                .all()
            )
        if current_month:
            if isinstance(current_month, dict):
                current_month = current_month.get('month')
            part_1, part_2 = self.__calculate_date_for_agent_withdraw(current_month)
            return (
                session.query(WithdrawModel)
                .order_by(asc(WithdrawModel.time_created))
                .filter(WithdrawModel.agent_source_id == agent.id)
                .filter(WithdrawModel.time_created.between(part_1, part_2))
                .all()
            )
        return (
            session.query(WithdrawModel)
            .order_by(asc(WithdrawModel.time_created))
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

    @staticmethod
    def __calculate_date_for_agent_withdraw(month):
        import datetime

        month_number = datetime.datetime.strptime(month, "%B").month

        year = datetime.date.today().year

        first_day = datetime.date(year, month_number, 1)

        if month_number == 12:
            last_day = datetime.date(year, month_number, 31)
        else:
            next_month_first_day = datetime.date(year, month_number + 1, 1)
            last_day = next_month_first_day - datetime.timedelta(days=1)

        last_day_plus_one = last_day + datetime.timedelta(days=1)

        first_day_str = first_day.strftime('%Y-%m-%d')
        last_day_plus_one_str = last_day_plus_one.strftime('%Y-%m-%d')
        return first_day_str, last_day_plus_one_str

    @staticmethod
    def get_all_for_xlsx():

        query = session.query(
            WithdrawModel.summa,
            LoanAdminsModel.admin_username,
            WithdrawModel.time_created
        ).join(
            LoanAdminsModel, LoanAdminsModel.id == WithdrawModel.agent_source_id
        )
        return query.all()


withdraw_cruds = WithdrawalCruds()
