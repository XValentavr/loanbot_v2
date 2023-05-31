import uuid
from datetime import timedelta
from typing import Optional

from sqlalchemy import asc

from create_engine import session
from cruds.source_of_income_cruds import source_of_income_cruds
from models.earning_model import EarningsModel


class EarningsCruds:
    @staticmethod
    def insert_source(summa: str, comment: str,
                      agent_id: Optional[str],
                      source_id: Optional[str],
                      currency: str,
                      is_other_source: str):
        source_name = source_of_income_cruds.get_source_by_source_id(source_id)
        source = EarningsModel(summa=summa,
                               comment=comment,
                               agent_source_id=agent_id,
                               income_source_id=source_id,
                               currency=currency,
                               is_other_source=is_other_source,
                               source_name=source_name.source)

        source.id = uuid.uuid4()

        session.add(source)
        session.commit()
        return source

    @staticmethod
    def get_earning_by_agent_id(agent_id: uuid.UUID) -> EarningsModel:
        return (
            session.query(EarningsModel)
            .order_by(asc(EarningsModel.time_created))
            .filter(EarningsModel.agent_source_id == agent_id)
            .all()
        )

    @staticmethod
    def get_earnings_history_by_date(agent_id: uuid.UUID, start: int, end: int, date_to_check) -> EarningsModel:
        if isinstance(date_to_check, list):
            interval_start = date_to_check[0].strftime("%Y-%m-%d")
            interval_end = (date_to_check[1] + timedelta(days=1)).strftime("%Y-%m-%d")

            return (
                session.query(EarningsModel)
                .order_by(asc(EarningsModel.time_created))
                .filter(EarningsModel.agent_source_id == agent_id)
                .filter(EarningsModel.time_created.between(interval_start, interval_end))
                .all()
            )
        earnings = (
            session.query(EarningsModel)
            .order_by(asc(EarningsModel.time_created))
            .filter(EarningsModel.agent_source_id == agent_id)
            .filter(EarningsModel.time_created < date_to_check)
            .all()
        )
        return earnings[start:end]


earnings_cruds = EarningsCruds()
