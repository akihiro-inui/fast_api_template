from pydantic import BaseModel
from typing import Optional


class AudioSchema(BaseModel):
    """
    Audio database table schema
    It holds all column names and relationship to other tables
    """
    md5: str
    file_name: str
    audio_format_id: str
    duration: int
    organization_id: str
    custom_property: str
    created_at: Optional[str]
    class Config:
        orm_mode = True


class AudioCreate(BaseModel):
    """
    Fields information needed for POST
    """
    md5: str
    file_name: str
    audio_format_id: str
    duration: int
    organization_id: str
    custom_property: str
    created_at: Optional[str]


class AudioUpdate(BaseModel):
    """
    Fields information needed for Update
    """
    md5: str
    file_name: Optional[str]
    audio_format_id: Optional[str]
    duration: Optional[int]
    organization_id: Optional[str]
    custom_property: Optional[str]


class AudioDelete(BaseModel):
    """
    Fields information needed for Delete
    """
    md5: str
