import uuid

from create_engine import session
from models.sources_of_income_model import SourcesOfIncomeModel


class SourceOfIncomeCruds:
    @staticmethod
    def insert_source(source: str):
        source_income = SourcesOfIncomeModel(source=source)

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


source_of_income_cruds = SourceOfIncomeCruds()
