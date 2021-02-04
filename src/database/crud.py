from sqlalchemy.orm import Session
from src.database.base import SessionLocal
from src.utils.common_logger import logger


def delete_table_rows(Model, db: Session = SessionLocal()) -> int:
    """
    Delete contents table by name
    :param Model: Data model class
    :param db: DB session
    :return: Number of deleted rows
    """
    try:
        # Delete all rows
        num_rows_deleted = db.query(Model).delete()
        db.commit()
        logger.info(f"Deleted {num_rows_deleted} rows")
        return num_rows_deleted
    except Exception as err:
        logger.error(err)
        db.rollback()
