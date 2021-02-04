from pydantic import BaseModel
from typing import Optional


class AnnotationTypeSchema(BaseModel):
    """
    AnnotationTypes database table schema
    It holds all column names and relationship to other tables
    """
    id: Optional[str]
    objective_name: str
    label_name: str
    value_type: str
    created_at: Optional[str]

    class Config:
        orm_mode = True


class AnnotationTypeCreate(BaseModel):
    """
    Fields information needed for POST
    """
    id: Optional[str]
    objective_name: str
    label_name: str
    value_type: str


class AnnotationTypeUpdate(BaseModel):
    """
    Fields information needed for Update
    """
    id: str
    objective_name: Optional[str]
    label_name: Optional[str]
    value_type: Optional[str]


class AnnotationTypeDelete(BaseModel):
    """
    Fields information needed for Delete
    """
    id: str
