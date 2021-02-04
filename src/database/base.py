import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.utils.config_reader import CFG
from src.utils.common_logger import logger


# Setup DB connector
engine = create_engine(f"postgresql://{CFG.DB_USER}:{CFG.DB_PASSWORD}@{CFG.DB_HOST}/{CFG.DB_NAME}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        yield db
    except Exception as err:
        logger.error(f"Failed to connect to database: {err}")
    finally:
        db.close()
