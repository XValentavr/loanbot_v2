import uuid
from typing import Union
from datetime import timedelta

from sqlalchemy import extract, func, asc, and_

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
    def get_source_by_source_id(source_id: uuid.UUID) -> SourcesOfIncomeModel:
        return (
            session.query(SourcesOfIncomeModel)
            .filter(SourcesOfIncomeModel.id == source_id)
            .first()
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
        interval_start = date_to_check[0].strftime("%Y-%m-%d")
        interval_end = (date_to_check[1] + timedelta(days=1)).strftime("%Y-%m-%d")

        return (
            session.query(EarningsModel)
            .join(EarningsModel.agent_id)
            .join(EarningsModel.source_id)
            .order_by(asc(EarningsModel.time_created))
            .filter(LoanAdminsModel.admin_username == username)
            .filter(and_(EarningsModel.time_created >= interval_start, EarningsModel.time_created <= interval_end))
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
        interval_end = date_to_check.strftime("%Y-%m-%d")
        return (session.query(
            extract('month', EarningsModel.time_created).label('month'),
            extract('year', EarningsModel.time_created).label('year'),
            EarningsModel.currency,
            func.sum(EarningsModel.summa).label('total')
        ).join(EarningsModel.agent_id)
                .join(EarningsModel.source_id)
                .filter(LoanAdminsModel.admin_username == username)
                .filter(EarningsModel.time_created < interval_end)
                .group_by('year', 'month', EarningsModel.currency)
                .all())


source_of_income_cruds = SourceOfIncomeCruds()
