from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from models.admins import LoanAdminsModel
from models.base_model import BaseModel


class SourcesOfIncomeModel(BaseModel):
    __tablename__ = "sources_of_income"

    source = Column(String(100), nullable=False)
    percent = Column(String(20), nullable=False)
    agent_id = relationship(LoanAdminsModel, backref="sources_of_income")

    agent_source_id = Column(
        String(100),
        ForeignKey("loan_admins.id"),
        nullable=True,
        unique=False,
    )

    is_active = Column(Boolean, default=True)
