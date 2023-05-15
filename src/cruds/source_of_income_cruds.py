import uuid
from typing import Union

from sqlalchemy import extract, func, asc

from create_engine import session
from models.admins import LoanAdminsModel
from models.earning_model import EarningsModel
from models.sources_of_income_model import SourcesOfIncomeModel


class SourceOfIncomeCruds:
    @staticmethod
    def insert_source(source: str, percent: str):
        source_income = SourcesOfIncomeModel(source=source, percent=percent)

        source_income.id = uuid.uuid4()

        session.add(source_income)
        session.commit()

    @staticmethod
    def get_all_sources() -> SourcesOfIncomeModel:
        return (
            session.query(SourcesOfIncomeModel).all()
        )

    @staticmethod
    def get_source_by_agent_id(agent_id: uuid.UUID) -> SourcesOfIncomeModel:
        return (
            session.query(SourcesOfIncomeModel)
            .filter(SourcesOfIncomeModel.agent_source_id == agent_id)
            .all()
        )

    @staticmethod
    def get_source_by_source_name(source_name: str) -> SourcesOfIncomeModel:
        return (
            session.query(SourcesOfIncomeModel)
            .filter(SourcesOfIncomeModel.source == source_name)
            .first()
        )

    @staticmethod
    def get_source_percent_and_summa_by_username_last_two_weeks(username: str, date_to_check) -> Union[EarningsModel]:
        return (
            session.query(EarningsModel)
            .join(EarningsModel.agent_id)
            .join(EarningsModel.source_id)
            .order_by(asc(EarningsModel.time_created))
            .filter(LoanAdminsModel.admin_username == username)
            .filter(EarningsModel.time_created >= date_to_check)
            .all()
        )

    @staticmethod
    def get_source_percent_all_agent_profit_by_limit(username: str) -> Union[EarningsModel]:
        return (
            session.query(EarningsModel)
            .join(EarningsModel.agent_id)
            .join(EarningsModel.source_id)
            .order_by(asc(EarningsModel.time_created))
            .filter(LoanAdminsModel.admin_username == username)
            .all()
        )

    @staticmethod
    def get_source_percent_and_summa_by_username_other_date(username: str, date_to_check) -> Union[EarningsModel]:
        return (session.query(
            extract('month', EarningsModel.time_created).label('month'),
            extract('year', EarningsModel.time_created).label('year'),
            EarningsModel.currency,
            func.sum(EarningsModel.summa).label('total')
        ).join(EarningsModel.agent_id)
                .join(EarningsModel.source_id)
                .filter(LoanAdminsModel.admin_username == username)
                .filter(EarningsModel.time_created < date_to_check)
                .group_by('year', 'month', EarningsModel.currency)
                .all())


source_of_income_cruds = SourceOfIncomeCruds()
