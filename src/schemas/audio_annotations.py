from pydantic import BaseModel
from typing import Optional


class AudioAnnotationsSchema(BaseModel):
    """
    AudioAnnotations database table schema
    It holds all column names and relationship to other tables
    """
    id: str
    annotation_type_id: str
    annotator_id: str
    dataset_id: str
    value: str
    start_time: str
    stop_time: str
    created_at: str
    md5: str
    version: int
    class Config:
        orm_mode = True


class AudioAnnotationsCreate(BaseModel):
    """
    Fields information needed for POST
    """
    id: str
    annotation_type_id: str
    annotator_id: str
    dataset_id: str
    value: str
    start_time: str
    stop_time: str
    created_at: Optional[str]
    md5: str
    version: int


class AudioAnnotationsUpdate(BaseModel):
    """
    Fields information needed for Update
    """
    id: str
    annotation_type_id: Optional[str]
    annotator_id: Optional[str]
    dataset_id: Optional[str]
    value: Optional[str]
    start_time: Optional[str]
    stop_time: Optional[str]
    md5: Optional[str]
    version: Optional[int]


class AudioAnnotationsDelete(BaseModel):
    """
    Fields information needed for Delete
    """
    id: str
    md5: Optional[str]
