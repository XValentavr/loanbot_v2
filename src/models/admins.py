from sqlalchemy import Column, String, Boolean

from models.base_model import BaseModel


class LoanAdminsModel(BaseModel):
    __tablename__ = "loan_admins"

    admin_username = Column(String(100), nullable=False)
    admin_password = Column(String(255), nullable=False)
    is_login = Column(Boolean, default=False)
