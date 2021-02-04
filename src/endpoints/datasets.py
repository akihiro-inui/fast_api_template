from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from src.schemas.datasets import DatasetSchema, DatasetCreate, DatasetDelete, DatasetUpdate
from fastapi import Depends
from src.database.base import get_db
from src.models.datasets import DatasetsModel
from fastapi import APIRouter
router = APIRouter()


@router.get("/datasets", response_model=List[DatasetSchema])
def get_all_datasets(db: Session = Depends(get_db)):
    """
    GET all datasets
    :param db: DB session
    :return: ALl annotator entries
    """
    return [{"id": str(dataset.id), "name": dataset.name, "type": dataset.type, "created_at": str(dataset.created_at), "description": dataset.description} for dataset in db.query(DatasetsModel).all()]


@router.get("/datasets/name/{dataset_name}", response_model=DatasetSchema)
def get_one_dataset_by_name(dataset_name: str, db: Session = Depends(get_db)):
    """
    GET one dataset by name
    :param dataset_name: Dataset name to get
    :param db: DB session
    :return: Retrieved annotator entry
    """
    try:
        # Get dataset by name
        dataset = db.query(DatasetsModel).filter(DatasetsModel.name == dataset_name).one()
        return {"id": str(dataset.id), "name": dataset.name, "type": dataset.type, "created_at": str(dataset.created_at), "description": dataset.description}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{dataset_name} does not exist")


@router.get("/datasets/id/{dataset_id}", response_model=DatasetSchema)
def get_one_dataset_by_id(dataset_id: str, db: Session = Depends(get_db)):
    """
    GET one dataset by UUID
    :param dataset_id: Dataset ID to get
    :param db: DB session
    :return: Retrieved annotator entry
    """
    try:
        # Get dataset by name
        dataset = db.query(DatasetsModel).filter(DatasetsModel.id == dataset_id).one()
        return {"id": str(dataset.id), "name": dataset.name, "type": dataset.type, "created_at": str(dataset.created_at), "description": dataset.description}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{dataset_id} does not exist")


@router.post("/datasets", response_model=DatasetCreate)
def post_one_dataset(dataset: DatasetCreate, db: Session = Depends(get_db)):
    """
    POST one annotator
    It reads parameters from the request field and add missing fields from default values defined in the model
    :param dataset: Dataset class that contains all columns in the table
    :param db: DB session
    :return: Created annotator entry
    """
    # Create Annotator Model
    dataset_to_create = DatasetsModel(**dataset.dict())

    # Commit to DB
    db.add(dataset_to_create)
    db.commit()
    db.refresh(dataset_to_create)
    return {"id": str(dataset.id), "name": dataset.name, "type": dataset.type, "created_at": str(dataset.created_at), "description": dataset.description}


@router.put("/datasets", response_model=DatasetSchema)
def put_one_dataset(dataset: DatasetUpdate, db: Session = Depends(get_db)):
    """
    PUT one dataset
    It reads parameters from the request field and update finds the entry and update it
    :param dataset: DatasetUpdate class that contains requested field to update
    :param db: DB session
    :return: Updated dataset entry
    """
    try:
        # Get annotator by ID
        dataset_to_put = db.query(DatasetsModel).filter(DatasetsModel.id == dataset.id).one()

        # Update model class variable for requested fields
        for var, value in vars(dataset).items():
            setattr(dataset_to_put, var, value) if value else None

        # Commit to DB
        db.add(dataset_to_put)
        db.commit()
        db.refresh(dataset_to_put)
        return {"id": str(dataset_to_put.id), "name": dataset_to_put.name, "type": dataset_to_put.type, "created_at": str(dataset_to_put.created_at), "description": dataset_to_put.description}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{dataset.id} does not exist")


@router.delete("/datasets/id/{dataset_id}", response_model=DatasetDelete)
def delete_one_dataset_by_id(dataset_id: str, db: Session = Depends(get_db)):
    """
    DELETE one dataset by name
    It reads parameters from the request field, finds the entry and delete it
    :param dataset_id: Dataset ID
    :param db: DB session
    :return: Deleted annotator entry
    """
    try:
        # Delete entry
        affected_rows = db.query(DatasetsModel).filter(DatasetsModel.id == dataset_id).delete()
        if not affected_rows:
            raise sqlalchemy.orm.exc.NoResultFound
        # Commit to DB
        db.commit()
        return {"id": str(dataset_id)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{dataset_id} does not exist")
