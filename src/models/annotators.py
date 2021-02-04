import uuid
from src.database.base import Base
from sqlalchemy import Column, VARCHAR, TIMESTAMP, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class AnnotatorModel(Base):
    """
    Define Annotator database table ORM model
    """
    __tablename__ = "annotators"

    # Register columns
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True, index=True)
    name = Column(VARCHAR, unique=False, index=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    created_at = Column(TIMESTAMP, default=func.now())
    age = Column(Integer)
    gender = Column(VARCHAR, unique=False)
