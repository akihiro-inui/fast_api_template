import uuid
from src.database.base import Base
from sqlalchemy import Column, VARCHAR, TIMESTAMP, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class AudioModel(Base):
    """
    Define Audio database table ORM model
    """
    __tablename__ = "audio"

    # Register columns
    md5 = Column(VARCHAR, unique=True, primary_key=True, index=True)
    file_name = Column(VARCHAR, unique=False, index=True)
    audio_format_id = Column(UUID(as_uuid=True), ForeignKey("audio_format.id"))
    duration = Column(Float)
    created_at = Column(TIMESTAMP, default=func.now())
    custom_property = Column(VARCHAR)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
