from pydantic import BaseModel
from typing import Optional


class DatasetSchema(BaseModel):
    """
    Dataset database table schema
    It holds all column names and relationship to other tables
    """
    id: str
    name: str
    type: str
    created_at: str
    description: str
    class Config:
        orm_mode = True


class DatasetCreate(BaseModel):
    """
    Fields information needed for POST
    """
    id: str
    name: str
    type: str
    created_at: Optional[str]
    description: Optional[str]


class DatasetUpdate(BaseModel):
    """
    Fields information needed for Update
    """
    id: str
    name: Optional[str]
    type: Optional[str]
    description: Optional[str]


class DatasetDelete(BaseModel):
    """
    Fields information needed for Delete
    """
    id: str
