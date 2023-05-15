import uuid
from typing import Optional

from sqlalchemy import desc

from create_engine import session
from models.earning_model import EarningsModel


class EarningsCruds:
    @staticmethod
    def insert_source(summa: str, comment: str,
                      agent_id: Optional[str],
                      source_id: Optional[str],
                      currency: str,
                      is_other_source: str):
        source = EarningsModel(summa=summa,
                               comment=comment,
                               agent_source_id=agent_id,
                               income_source_id=source_id,
                               currency=currency,
                               is_other_source=is_other_source)

        source.id = uuid.uuid4()

        session.add(source)
        session.commit()

    @staticmethod
    def get_earning_by_agent_id(agent_id: uuid.UUID) -> EarningsModel:
        return (
            session.query(EarningsModel)
            .order_by(desc(EarningsModel.time_created))
            .filter(EarningsModel.agent_source_id == agent_id)
            .all()
        )

    @staticmethod
    def get_earnings_history(agent_id: uuid.UUID, start: int, end: int) -> EarningsModel:
        earnings = (
            session.query(EarningsModel)
            .order_by(desc(EarningsModel.time_created))
            .filter(EarningsModel.agent_source_id == agent_id)
            .all()
        )
        return earnings[start:end]


earnings_cruds = EarningsCruds()
