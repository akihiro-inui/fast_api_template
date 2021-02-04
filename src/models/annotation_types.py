import uuid
from src.database.base import Base
from sqlalchemy import Column, VARCHAR, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class AnnotationTypeModel(Base):
    """
    Define AnnotationType database table ORM model
    """
    __tablename__ = "annotation_types"

    # Register columns
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True, index=True)
    objective_name = Column(VARCHAR, unique=False, index=True)
    label_name = Column(VARCHAR, unique=False, index=True)
    value_type = Column(VARCHAR, unique=False, index=True)
    created_at = Column(TIMESTAMP, default=func.now())
