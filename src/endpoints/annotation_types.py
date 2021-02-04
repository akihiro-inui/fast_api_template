from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from src.schemas.annotation_types import AnnotationTypeSchema, AnnotationTypeCreate, AnnotationTypeUpdate, AnnotationTypeDelete
from fastapi import Depends
from src.database.base import get_db
from src.models.annotation_types import AnnotationTypeModel
from fastapi import APIRouter
router = APIRouter()


@router.get("/annotation_types", response_model=List[AnnotationTypeSchema])
def get_all_annotation_types(db: Session = Depends(get_db)):
    """
    GET all annotation_types
    :param db: DB session
    :return: ALl annotation_type entries
    """
    return [{"id": str(annotation_type.id), "objective_name": annotation_type.objective_name, "label_name": annotation_type.label_name, "value_type": annotation_type.value_type, "created_at": str(annotation_type.created_at)} for annotation_type in db.query(AnnotationTypeModel).all()]


@router.get("/annotation_types/id/{annotation_type_id}", response_model=AnnotationTypeSchema)
def get_one_annotation_type_by_id(annotation_type_id: str, db: Session = Depends(get_db)):
    """
    GET one annotation_type by ID
    :param annotation_type_id: annotation_type ID to get
    :param db: DB session
    :return: Retrieved annotation_type entry
    """
    try:
        # Get annotation_type by name
        annotation_type = db.query(AnnotationTypeModel).filter(AnnotationTypeModel.id == annotation_type_id).one()
        return {"id": str(annotation_type.id), "objective_name": annotation_type.objective_name, "label_name": annotation_type.label_name, "value_type": annotation_type.value_type, "created_at": str(annotation_type.created_at)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{annotation_type_id} does not exist")


@router.post("/annotation_types", response_model=AnnotationTypeCreate)
def post_one_annotation_type(annotation_type: AnnotationTypeCreate, db: Session = Depends(get_db)):
    """
    POST one annotation_type
    It reads parameters from the request field and add missing fields from default values defined in the model
    :param annotation_type: AnnotatorBase class that contains all columns in the table
    :param db: DB session
    :return: Created annotation_type entry
    """
    # Create annotation_type Model
    annotator_to_create = AnnotationTypeModel(**annotation_type.dict())

    # Commit to DB
    db.add(annotator_to_create)
    db.commit()
    db.refresh(annotator_to_create)
    return {"id": str(annotator_to_create.id), "objective_name": annotator_to_create.objective_name, "label_name": annotator_to_create.label_name, "value_type": annotator_to_create.value_type, "created_at": str(annotator_to_create.created_at)}


@router.put("/annotation_types", response_model=AnnotationTypeSchema)
def put_one_annotation_type(annotation_type: AnnotationTypeUpdate, db: Session = Depends(get_db)):
    """
    PUT one annotation_type
    It reads parameters from the request field and update finds the entry and update it
    :param annotation_type: AnnotatorUpdate class that contains requested field to update
    :param db: DB session
    :return: Updated annotation_type entry
    """
    try:
        # Get annotation_type by ID
        annotation_type_to_put = db.query(AnnotationTypeModel).filter(AnnotationTypeModel.id == annotation_type.id).one()

        # Update model class variable for requested fields
        for var, value in vars(annotation_type).items():
            setattr(annotation_type_to_put, var, value) if value else None

        # Commit to DB
        db.add(annotation_type_to_put)
        db.commit()
        db.refresh(annotation_type_to_put)
        return {"id": str(annotation_type_to_put.id), "objective_name": annotation_type_to_put.objective_name,
                "label_name": annotation_type_to_put.label_name, "value_type": annotation_type_to_put.value_type,
                "created_at": str(annotation_type_to_put.created_at)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{annotation_type.id} does not exist")


@router.delete("/annotation_types/id/{annotation_type_id}", response_model=AnnotationTypeDelete)
def delete_one_annotation_type_by_id(annotation_type_id: str, db: Session = Depends(get_db)):
    """
    DELETE one annotation_type by ID
    It reads parameters from the request field, finds the entry and delete it
    :param annotation_type_id: annotation_type ID to delete
    :param db: DB session
    :return: Deleted annotation_type entry
    """
    try:
        # Delete entry
        affected_rows = db.query(AnnotationTypeModel).filter(AnnotationTypeModel.id == annotation_type_id).delete()
        if not affected_rows:
            raise sqlalchemy.orm.exc.NoResultFound
        # Commit to DB
        db.commit()
        return {"id": str(annotation_type_id)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{annotation_type_id} does not exist")
