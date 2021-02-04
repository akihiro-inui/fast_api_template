from pydantic import BaseModel
from typing import Optional


class OrganizationSchema(BaseModel):
    """
    Organization database table schema
    It holds all column names and relationship to other tables
    """
    id: Optional[str]
    name: str
    created_at: Optional[str]

    class Config:
        orm_mode = True


class OrganizationCreate(BaseModel):
    """
    Fields information needed for POST
    """
    id: Optional[str]
    name: str


class OrganizationUpdate(BaseModel):
    """
    Fields information needed for Update
    """
    id: str
    name: Optional[str]


class OrganizationDelete(BaseModel):
    """
    Fields information needed for Delete
    """
    id: str
