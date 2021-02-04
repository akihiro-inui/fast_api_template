from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from src.schemas.organizations import OrganizationSchema, OrganizationCreate, OrganizationUpdate, OrganizationDelete
from fastapi import Depends
from src.database.base import get_db
from src.models.organizations import OrganizationModel
from fastapi import APIRouter
router = APIRouter()


@router.get("/organizations", response_model=List[OrganizationSchema])
def get_all_organizations(db: Session = Depends(get_db)):
    """
    GET all organizations
    :param db: DB session
    :return: ALl organization entries
    """
    return [{"id": str(organization.id), "name": organization.name, "created_at": str(organization.created_at)} for organization in db.query(OrganizationModel).all()]


@router.get("/organizations/name/{organization_name}", response_model=OrganizationSchema)
def get_one_organization_by_name(organization_name: str, db: Session = Depends(get_db)):
    """
    GET one organization by name
    :param organization_name: Organization name to get
    :param db: DB session
    :return: Retrieved organization entry
    """
    try:
        organization = db.query(OrganizationModel).filter(OrganizationModel.name == organization_name).one()
        return {"id": str(organization.id), "name": organization.name, "created_at": str(organization.created_at)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{organization_name} does not exist")


@router.get("/organizations/id/{organization_id}", response_model=OrganizationSchema)
def get_one_organization_by_id(organization_id: str, db: Session = Depends(get_db)):
    """
    GET one organization by ID
    :param organization_id: Organization name to get
    :param db: DB session
    :return: Retrieved organization entry
    """
    try:
        organization = db.query(OrganizationModel).filter(OrganizationModel.id == organization_id).one()
        return {"id": str(organization.id), "name": organization.name, "created_at": str(organization.created_at)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{organization_id} does not exist")


@router.post("/organizations", response_model=OrganizationCreate)
def post_one_organization(organization: OrganizationCreate, db: Session = Depends(get_db)):
    """
    POST one organization
    It reads parameters from the request field and add missing fields from default values defined in the model
    :param organization: OrganizationBase class that contains all columns in the table
    :param db: DB session
    :return: Created organization entry
    """
    # Create Organization Model
    organization_to_create = OrganizationModel(**organization.dict())

    # Commit to DB
    db.add(organization_to_create)
    db.commit()
    db.refresh(organization_to_create)
    return {"id": str(organization_to_create.id), "name": organization_to_create.name, "created_at": str(organization_to_create.created_at)}


@router.put("/organizations", response_model=OrganizationSchema)
def put_one_organization(organization: OrganizationUpdate, db: Session = Depends(get_db)):
    """
    PUT one organization
    It reads parameters from the request field and update finds the entry and update it
    :param organization: OrganizationUpdate class
    :param db: DB session
    :return: Updated organization entry
    """
    try:
        # Get organization by ID
        organization_to_put = db.query(OrganizationModel).filter(OrganizationModel.id == organization.id).one()

        # Update model class variable for requested fields
        for var, value in vars(organization).items():
            setattr(organization_to_put, var, value) if value else None

        # Commit to DB
        db.add(organization_to_put)
        db.commit()
        db.refresh(organization_to_put)
        return {"id": str(organization_to_put.id), "name": organization_to_put.name, "created_at": str(organization_to_put.created_at)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{organization.id} does not exist")


@router.delete("/organizations/id/{organization_id}", response_model=OrganizationDelete)
def delete_one_organization(organization_id: str, db: Session = Depends(get_db)):
    """
    DELETE one organization by ID
    It reads parameters from the request field, finds the entry and delete it
    :param organization_id: Organization ID to delete
    :param db: DB session
    :return: Deleted organization entry
    """
    try:
        # Delete entry
        affected_rows = db.query(OrganizationModel).filter(OrganizationModel.id == organization_id).delete()
        if not affected_rows:
            raise sqlalchemy.orm.exc.NoResultFound
        # Commit to DB
        db.commit()
        return {"id": str(organization_id)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{organization_id} does not exist")