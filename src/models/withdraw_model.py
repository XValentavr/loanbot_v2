from sqlalchemy import Column, String, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship

from models.admins import LoanAdminsModel
from models.base_model import BaseModel


class WithdrawModel(BaseModel):
    __tablename__ = "withdraw"

    summa = Column(String(155), nullable=False)
    agent_id = relationship(LoanAdminsModel, backref="withdraw")

    agent_source_id = Column(
        String(100),
        ForeignKey("loan_admins.id"),
        nullable=True,
        unique=False,
    )
    time_created = Column(DateTime(timezone=True), server_default=func.now())
