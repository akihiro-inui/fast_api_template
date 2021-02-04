from pydantic import BaseModel
from typing import Optional


class AnnotatorSchema(BaseModel):
    """
    Annotator database table schema
    It holds all column names and relationship to other tables
    """
    id: Optional[str]
    name: str
    age: int
    gender: str
    organization_id: str
    created_at: Optional[str]

    class Config:
        orm_mode = True


class AnnotatorCreate(BaseModel):
    """
    Fields information needed for POST
    """
    id: Optional[str]
    name: str
    age: int
    gender: str
    organization_id: str


class AnnotatorUpdate(BaseModel):
    """
    Fields information needed for Update
    """
    id: str
    name: Optional[str]
    age: Optional[int]
    gender: Optional[int]
    organization_id: Optional[str]


class AnnotatorDelete(BaseModel):
    """
    Fields information needed for Delete
    """
    id: str
