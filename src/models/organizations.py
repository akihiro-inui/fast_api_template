import uuid
from src.database.base import Base
from sqlalchemy import Column, VARCHAR, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class OrganizationModel(Base):
    """
    Define Organization database table ORM model
    """
    __tablename__ = "organizations"

    # Register columns
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True, index=True)
    name = Column(VARCHAR, unique=True, index=True)
    created_at = Column(TIMESTAMP, default=func.now())
