import uuid
from src.database.base import Base
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import UUID


class AudioFormatModel(Base):
    """
    Define AudioFormat database table ORM model
    """
    __tablename__ = "audio_format"

    # Register columns
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True, index=True)
    bit_rate = Column(Integer)
    sample_rate = Column(Integer)
    channels = Column(Integer)
