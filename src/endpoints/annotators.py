from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from src.schemas.annotators import AnnotatorSchema, AnnotatorCreate, AnnotatorUpdate, AnnotatorDelete
from fastapi import Depends
from src.database.base import get_db
from src.models.annotators import AnnotatorModel
from fastapi import APIRouter
router = APIRouter()


@router.get("/annotators", response_model=List[AnnotatorSchema])
def get_all_annotators(db: Session = Depends(get_db)):
    """
    GET all annotators
    :param db: DB session
    :return: ALl annotator entries
    """
    return [{"id": str(annotator.id), "name": annotator.name, "age": annotator.age, "gender": annotator.gender, "organization_id": str(annotator.organization_id), "created_at": str(annotator.created_at)} for annotator in db.query(AnnotatorModel).all()]


@router.get("/annotators/name/{annotator_name}", response_model=AnnotatorSchema)
def get_one_annotator_by_name(annotator_name: str, db: Session = Depends(get_db)):
    """
    GET one annotator by name
    :param annotator_name: Annotator name to get
    :param db: DB session
    :return: Retrieved annotator entry
    """
    try:
        # Get annotator by name
        annotator = db.query(AnnotatorModel).filter(AnnotatorModel.name == annotator_name).one()
        return {"id": str(annotator.id), "name": annotator.name, "age": annotator.age, "gender": annotator.gender, "organization_id": str(annotator.organization_id), "created_at": str(annotator.created_at)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{annotator_name} does not exist")


@router.get("/annotators/id/{annotator_id}", response_model=AnnotatorSchema)
def get_one_annotator_by_id(annotator_id: str, db: Session = Depends(get_db)):
    """
    GET one annotator by ID
    :param annotator_id: Annotator ID to get
    :param db: DB session
    :return: Retrieved annotator entry
    """
    try:
        # Get annotator by name
        annotator = db.query(AnnotatorModel).filter(AnnotatorModel.id == annotator_id).one()
        return {"id": str(annotator.id), "name": annotator.name, "age": annotator.age, "gender": annotator.gender, "organization_id": str(annotator.organization_id), "created_at": str(annotator.created_at)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{annotator_id} does not exist")


@router.post("/annotators", response_model=AnnotatorCreate)
def post_one_annotator(annotator: AnnotatorCreate, db: Session = Depends(get_db)):
    """
    POST one annotator
    It reads parameters from the request field and add missing fields from default values defined in the model
    :param annotator: AnnotatorBase class that contains all columns in the table
    :param db: DB session
    :return: Created annotator entry
    """
    # Create Annotator Model
    annotator_to_create = AnnotatorModel(**annotator.dict())

    # Commit to DB
    db.add(annotator_to_create)
    db.commit()
    db.refresh(annotator_to_create)
    return {"id": str(annotator_to_create.id), "name": annotator_to_create.name, "age": annotator.age, "gender": annotator.gender, "organization_id": annotator.organization_id, "created_at": str(annotator_to_create.created_at)}


@router.put("/annotators", response_model=AnnotatorSchema)
def put_one_annotator(annotator: AnnotatorUpdate, db: Session = Depends(get_db)):
    """
    PUT one annotator
    It reads parameters from the request field and update finds the entry and update it
    :param annotator: AnnotatorUpdate class that contains requested field to update
    :param db: DB session
    :return: Updated annotator entry
    """
    try:
        # Get annotator by ID
        annotator_to_put = db.query(AnnotatorModel).filter(AnnotatorModel.id == annotator.id).one()

        # Update model class variable for requested fields
        for var, value in vars(annotator).items():
            setattr(annotator_to_put, var, value) if value else None

        # Commit to DB
        db.add(annotator_to_put)
        db.commit()
        db.refresh(annotator_to_put)
        return {"id": str(annotator_to_put.id), "name": annotator_to_put.name, "age": annotator_to_put.age, "gender": annotator_to_put.gender, "organization_id": str(annotator_to_put.organization_id), "created_at": str(annotator_to_put.created_at)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{annotator.id} does not exist")


@router.delete("/annotators/id/{annotator_id}", response_model=AnnotatorDelete)
def delete_one_annotator_by_id(annotator_id: str, db: Session = Depends(get_db)):
    """
    DELETE one annotator by ID
    It reads parameters from the request field, finds the entry and delete it
    :param annotator_id: Annotator ID to delete
    :param db: DB session
    :return: Deleted annotator entry
    """
    try:
        # Delete entry
        affected_rows = db.query(AnnotatorModel).filter(AnnotatorModel.id == annotator_id).delete()
        if not affected_rows:
            raise sqlalchemy.orm.exc.NoResultFound
        # Commit to DB
        db.commit()
        return {"id": str(annotator_id)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{annotator_id} does not exist")
