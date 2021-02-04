import uuid
from src.database.base import Base
from sqlalchemy import Column, VARCHAR, TIMESTAMP, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class DatasetsModel(Base):
    """
    Define Datasets database table ORM model
    """
    __tablename__ = "datasets"

    # Register columns
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True, index=True)
    name = Column(VARCHAR, unique=True, index=True)
    type = Column(VARCHAR, unique=False, index=True)
    created_at = Column(TIMESTAMP, default=func.now())
    description = Column(VARCHAR, unique=False, index=True)
