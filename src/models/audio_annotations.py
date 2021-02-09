import uuid
from src.database.base import Base
from sqlalchemy import Column, VARCHAR, TIMESTAMP, Integer, ForeignKey, TIME
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class AudioAnnotationsModel(Base):
    """
    Define Audio database table ORM model
    """
    __tablename__ = "audio_annotations"

    # Register columns
    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, index=True)
    annotation_type_id = Column(UUID(as_uuid=True), ForeignKey("annotation_types.id"))
    annotator_id = Column(UUID(as_uuid=True), ForeignKey("annotators.id"))
    dataset_id = Column(UUID(as_uuid=True), ForeignKey("datasets.id"))
    value = Column(VARCHAR)
    start_time = Column(TIME)
    stop_time = Column(TIME)
    created_at = Column(TIMESTAMP, default=func.now())
    md5 = Column(VARCHAR, ForeignKey("audio.md5"))
    version = Column(Integer)
