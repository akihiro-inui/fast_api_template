from pydantic import BaseModel
from typing import Optional


class AudioFormatSchema(BaseModel):
    """
    AudioFormat database table schema
    It holds all column names and relationship to other tables
    """
    id: Optional[str]
    bit_rate: int
    sample_rate: int
    channels: int

    class Config:
        orm_mode = True


class AudioFormatCreate(BaseModel):
    """
    Fields information needed for POST
    """
    id: Optional[str]
    bit_rate: int
    sample_rate: int
    channels: int


class AudioFormatUpdate(BaseModel):
    """
    Fields information needed for Update
    """
    id: str
    bit_rate: Optional[int]
    sample_rate: Optional[int]
    channels: Optional[int]


class AudioFormatDelete(BaseModel):
    """
    Fields information needed for Delete
    """
    id: str
