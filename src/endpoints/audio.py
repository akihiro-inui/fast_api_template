from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from src.schemas.audio import AudioSchema, AudioCreate, AudioUpdate, AudioDelete
from fastapi import Depends
from src.database.base import get_db
from src.models.audio import AudioModel
from fastapi import APIRouter
router = APIRouter()


@router.get("/audio", response_model=List[AudioSchema])
def get_all_audio(db: Session = Depends(get_db)):
    """
    GET all audio
    :param db: DB session
    :return: ALl audio entries
    """
    return [{"md5": str(audio.md5), "file_name": audio.file_name, "audio_format_id": str(audio.audio_format_id), "duration": audio.duration, "custom_property": str(audio.custom_property), "organization_id": str(audio.organization_id), "created_at": str(audio.created_at)} for audio in db.query(AudioModel).all()]


@router.get("/audio/md5/{md5}", response_model=AudioSchema)
def get_one_audio_by_md5(md5: str, db: Session = Depends(get_db)):
    """
    GET one audio by md5
    :param md5: md5 of the audio file
    :param db: DB session
    :return: Retrieved audio entry
    """
    try:
        # Get audio by name
        audio = db.query(AudioModel).filter(AudioModel.md5 == md5).one()
        return {"md5": str(audio.md5), "file_name": audio.file_name, "audio_format_id": str(audio.audio_format_id), "duration": audio.duration, "custom_property": str(audio.custom_property), "organization_id": str(audio.organization_id), "created_at": str(audio.created_at)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{md5} does not exist")


@router.get("/audio/file_name/{file_name}", response_model=AudioSchema)
def get_one_audio_by_file_path(file_name: str, db: Session = Depends(get_db)):
    """
    GET one audio by file path
    :param file_name: Audio file path
    :param db: DB session
    :return: Retrieved audio entry
    """
    try:
        # Get audio by name
        audio = db.query(AudioModel).filter(AudioModel.file_name == file_name).one()
        return {"md5": str(audio.md5), "file_name": audio.file_name, "audio_format_id": str(audio.audio_format_id), "duration": audio.duration, "custom_property": str(audio.custom_property), "organization_id": str(audio.organization_id), "created_at": str(audio.created_at)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{file_name} does not exist")


@router.post("/audio", response_model=AudioCreate)
def post_one_audio(audio: AudioCreate, db: Session = Depends(get_db)):
    """
    POST one audio
    It reads parameters from the request field and add missing fields from default values defined in the model
    :param audio: Audio class that contains all columns in the table
    :param db: DB session
    :return: Created audio entry
    """
    # Create Audio Model
    audio_to_create = AudioModel(**audio.dict())

    # Commit to DB
    db.add(audio_to_create)
    db.commit()
    db.refresh(audio_to_create)
    return {"md5": str(audio.md5), "file_name": audio.file_name, "audio_format_id": str(audio.audio_format_id), "duration": audio.duration, "custom_property": str(audio.custom_property), "organization_id": str(audio.organization_id), "created_at": str(audio.created_at)}


@router.put("/audio", response_model=AudioSchema)
def put_one_audio(audio: AudioUpdate, db: Session = Depends(get_db)):
    """
    PUT one audio
    It reads parameters from the request field and update finds the entry and update it
    :param audio: AudioUpdate class that contains requested field to update
    :param db: DB session
    :return: Updated audio entry
    """
    try:
        # Get audio by ID
        audio_to_put = db.query(AudioModel).filter(AudioModel.md5 == audio.md5).one()

        # Update model class variable for requested fields
        for var, value in vars(audio).items():
            setattr(audio_to_put, var, value) if value else None

        # Commit to DB
        db.add(audio_to_put)
        db.commit()
        db.refresh(audio_to_put)
        return {"md5": str(audio_to_put.md5), "file_name": audio_to_put.file_name, "audio_format_id": str(audio_to_put.audio_format_id),
                "duration": audio_to_put.duration, "custom_property": str(audio_to_put.custom_property),
                "organization_id": str(audio_to_put.organization_id)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{audio.md5} does not exist")


@router.delete("/audio/md5/{md5}", response_model=AudioDelete)
def delete_one_audio_by_md5(md5: str, db: Session = Depends(get_db)):
    """
    DELETE one audio by md5
    It reads parameters from the request field, finds the entry and delete it
    :param md5: audio md5 to delete
    :param db: DB session
    :return: Deleted audio entry
    """
    try:
        # Delete entry
        affected_rows = db.query(AudioModel).filter(AudioModel.md5 == md5).delete()
        if not affected_rows:
            raise sqlalchemy.orm.exc.NoResultFound
        # Commit to DB
        db.commit()
        return {"md5": str(md5)}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{md5} does not exist")
