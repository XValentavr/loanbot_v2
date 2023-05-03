from sqlalchemy import Column, String, Boolean, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship

from models.admins import LoanAdminsModel
from models.base_model import BaseModel
from models.sources_of_income_model import SourcesOfIncomeModel


class EarningsModel(BaseModel):
    __tablename__ = "earnings_model"

    summa = Column(String(155), nullable=False)
    comment = Column(String(255), nullable=True)
    agent_id = relationship(LoanAdminsModel, backref="earnings_model")

    agent_source_id = Column(
        String(100),
        ForeignKey("loan_admins.id"),
        nullable=True,
        unique=False,
    )

    source_id = relationship(SourcesOfIncomeModel, backref="earnings_model")

    income_source_id = Column(
        String(100),
        ForeignKey("sources_of_income.id"),
        nullable=True,
        unique=False,
    )
    is_other_source = Column(String(255), nullable=True)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
