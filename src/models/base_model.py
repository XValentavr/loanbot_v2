import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeMeta, registry

from sqlalchemy.dialects.postgresql import UUID

mapper_registry = registry()


class Base(metaclass=DeclarativeMeta):
    __abstract__ = True

    registry = mapper_registry
    metadata = mapper_registry.metadata

    __init__ = mapper_registry.constructor


class BaseModel(Base):
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=uuid.uuid4())

    def __repr__(self):
        if self.id:
            return f"<{type(self)} with id {self.id}>"
        return super().__repr__()
