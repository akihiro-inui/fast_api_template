from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from src.schemas.audio_format import AudioFormatSchema, AudioFormatCreate, AudioFormatUpdate, AudioFormatDelete
from fastapi import Depends
from src.database.base import get_db
from src.models.audio_format import AudioFormatModel
from fastapi import APIRouter
router = APIRouter()


@router.get("/audio_format", response_model=List[AudioFormatSchema])
def get_all_audio_format(db: Session = Depends(get_db)):
    """
    GET all audio_format
    :param db: DB session
    :return: ALl audio_format entries
    """
    return [{"id": str(audio_format.id), "bit_rate": audio_format.bit_rate, "sample_rate": audio_format.sample_rate, "channels": audio_format.channels} for audio_format in db.query(AudioFormatModel).all()]


@router.get("/audio_format/id/{audio_format_id}", response_model=AudioFormatSchema)
def get_one_audio_format_by_id(audio_format_id: str, db: Session = Depends(get_db)):
    """
    GET one audio_format by ID
    :param audio_format_id: audio_format ID to get
    :param db: DB session
    :return: Retrieved audio_format entry
    """
    try:
        # Get audio_format by name
        audio_format = db.query(AudioFormatModel).filter(AudioFormatModel.id == audio_format_id).one()
        return {"id": str(audio_format.id), "bit_rate": audio_format.bit_rate, "sample_rate": audio_format.sample_rate, "channels": audio_format.channels}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{audio_format_id} does not exist")


@router.post("/audio_format", response_model=AudioFormatCreate)
def post_one_audio_format(audio_format: AudioFormatCreate, db: Session = Depends(get_db)):
    """
    POST one audio_format
    It reads parameters from the request field and add missing fields from default values defined in the model
    :param audio_format: AnnotatorBase class that contains all columns in the table
    :param db: DB session
    :return: Created audio_format entry
    """
    # Create audio_format Model
    annotator_to_create = AudioFormatModel(**audio_format.dict())

    # Commit to DB
    db.add(annotator_to_create)
    db.commit()
    db.refresh(annotator_to_create)
    return {"id": str(audio_format.id), "bit_rate": audio_format.bit_rate, "sample_rate": audio_format.sample_rate, "channels": audio_format.channels}


@router.put("/audio_format", response_model=AudioFormatSchema)
def put_one_audio_format(audio_format: AudioFormatUpdate, db: Session = Depends(get_db)):
    """
    PUT one audio_format
    It reads parameters from the request field and update finds the entry and update it
    :param audio_format: AnnotatorUpdate class that contains requested field to update
    :param db: DB session
    :return: Updated audio_format entry
    """
    try:
        # Get audio_format by ID
        annotator_to_put = db.query(AudioFormatModel).filter(AudioFormatModel.id == audio_format.id).one()

        # Update model class variable for requested fields
        for var, value in vars(audio_format).items():
            setattr(annotator_to_put, var, value) if value else None

        # Commit to DB
        db.add(annotator_to_put)
        db.commit()
        db.refresh(annotator_to_put)
        return {"id": str(annotator_to_put.id), "bit_rate": annotator_to_put.bit_rate, "sample_rate": annotator_to_put.sample_rate, "channels": annotator_to_put.channels}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{audio_format.id} does not exist")


@router.delete("/audio_format/id/{audio_format_id}", response_model=AudioFormatDelete)
def delete_one_audio_format_by_id(audio_format_id: str, db: Session = Depends(get_db)):
    """
    DELETE one audio_format by ID
    It reads parameters from the request field, finds the entry and delete it
    :param audio_format_id: audio_format ID to delete
    :param db: DB session
    :return: Deleted audio_format entry
    """
    try:
        # Delete entry
        affected_rows = db.query(AudioFormatModel).filter(AudioFormatModel.id == audio_format_id).delete()
        if not affected_rows:
            raise sqlalchemy.orm.exc.NoResultFound
        # Commit to DB
        db.commit()
        return {"id": str(audio_format_id)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{audio_format_id} does not exist")
