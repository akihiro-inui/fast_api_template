from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from src.schemas.audio_annotations import AudioAnnotationsSchema, AudioAnnotationsCreate, AudioAnnotationsDelete, AudioAnnotationsUpdate
from fastapi import Depends
from src.database.base import get_db
from src.models.audio_annotations import AudioAnnotationsModel
from fastapi import APIRouter
router = APIRouter()


@router.get("/audio_annotations", response_model=List[AudioAnnotationsSchema])
def get_all_audio_annotations(db: Session = Depends(get_db)):
    """
    GET all audio_annotations
    :param db: DB session
    :return: ALl audio_annotations entries
    """
    return [{"id": str(audio_annotations.id), "annotation_type_id": str(audio_annotations.annotation_type_id), "annotator_id": str(audio_annotations.annotator_id), "dataset_id": str(audio_annotations.dataset_id), "value": audio_annotations.value, "start_time": str(audio_annotations.start_time), "stop_time": str(audio_annotations.stop_time), "created_at": str(audio_annotations.created_at), "md5": str(audio_annotations.md5), "version": audio_annotations.version} for audio_annotations in db.query(AudioAnnotationsModel).all()]


@router.get("/audio_annotations/id/{id}", response_model=AudioAnnotationsSchema)
def get_one_audio_annotation_by_id(id: str, db: Session = Depends(get_db)):
    """
    GET one audio_annotations by md5
    :param id: UUID of the audio_annotation
    :param db: DB session
    :return: Retrieved audio_annotations entry
    """
    try:
        # Get audio_annotations by name
        audio_annotations = db.query(AudioAnnotationsModel).filter(AudioAnnotationsModel.id == id).one()
        return {"id": str(audio_annotations.id), "annotation_type_id": str(audio_annotations.annotation_type_id), "annotator_id": str(audio_annotations.annotator_id), "dataset_id": str(audio_annotations.dataset_id), "value": audio_annotations.value, "start_time": str(audio_annotations.start_time), "stop_time": str(audio_annotations.stop_time), "created_at": str(audio_annotations.created_at), "md5": str(audio_annotations.md5), "version": audio_annotations.version}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{id} does not exist")



@router.post("/audio_annotations", response_model=AudioAnnotationsCreate)
def post_one_audio_annotation(audio_annotations: AudioAnnotationsCreate, db: Session = Depends(get_db)):
    """
    POST one audio_annotations
    It reads parameters from the request field and add missing fields from default values defined in the model
    :param audio_annotations: audio_annotations class that contains all columns in the table
    :param db: DB session
    :return: Created audio_annotations entry
    """
    # Create audio_annotations Model
    audio_annotation_to_create = AudioAnnotationsModel(**audio_annotations.dict())

    # Commit to DB
    db.add(audio_annotation_to_create)
    db.commit()
    db.refresh(audio_annotation_to_create)
    return {"id": str(audio_annotations.id), "annotation_type_id": str(audio_annotations.annotation_type_id), "annotator_id": str(audio_annotations.annotator_id), "dataset_id": str(audio_annotations.dataset_id), "value": audio_annotations.value, "start_time": str(audio_annotations.start_time), "stop_time": str(audio_annotations.stop_time), "created_at": str(audio_annotations.created_at), "md5": str(audio_annotations.md5), "version": audio_annotations.version}


@router.put("/audio_annotations", response_model=AudioAnnotationsSchema)
def put_one_audio_annotation(audio_annotation: AudioAnnotationsUpdate, db: Session = Depends(get_db)):
    """
    PUT one audio_annotations
    It reads parameters from the request field and update finds the entry and update it
    :param audio_annotation: AudioAnnotationsUpdate class that contains requested field to update
    :param db: DB session
    :return: Updated audio_annotations entry
    """
    try:
        # Get audio_annotations by ID
        audio_annotation_to_put = db.query(AudioAnnotationsModel).filter(AudioAnnotationsModel.id == audio_annotation.id).one()

        # Update model class variable for requested fields
        for var, value in vars(audio_annotation).items():
            setattr(audio_annotation_to_put, var, value) if value else None

        # Commit to DB
        db.add(audio_annotation_to_put)
        db.commit()
        db.refresh(audio_annotation_to_put)
        return {"id": str(audio_annotation_to_put.id), "annotation_type_id": str(audio_annotation_to_put.annotation_type_id), "annotator_id": str(audio_annotation_to_put.annotator_id), "dataset_id": str(audio_annotation_to_put.dataset_id), "value": audio_annotation_to_put.value, "start_time": str(audio_annotation_to_put.start_time), "stop_time": str(audio_annotation_to_put.stop_time), "created_at": str(audio_annotation_to_put.created_at), "md5": str(audio_annotation_to_put.md5), "version": audio_annotation_to_put.version}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{audio_annotation.id} does not exist")


@router.delete("/audio_annotations/id/{id}", response_model=AudioAnnotationsDelete)
def delete_one_audio_annotation_by_id(id: str, db: Session = Depends(get_db)):
    """
    DELETE one audio_annotations by UUID
    It reads parameters from the request field, finds the entry and delete it
    :param id: audio_annotations md5 to delete
    :param db: DB session
    :return: Deleted audio_annotations entry
    """
    try:
        # Delete entry
        affected_rows = db.query(AudioAnnotationsModel).filter(AudioAnnotationsModel.id == id).delete()
        if not affected_rows:
            raise sqlalchemy.orm.exc.NoResultFound
        # Commit to DB
        db.commit()
        return {"id": str(id)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{id} does not exist")
