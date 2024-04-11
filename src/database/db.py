import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

file_config = pathlib.Path(__file__).parent.parent.joinpath("config/config.ini")
config = configparser.ConfigParser()
config.read(file_config)

username = config.get("DB", "USER")
password = config.get("DB", "PASSWORD")
database_name = config.get("DB", "DB_NAME")
domain = config.get("DB", "DOMAIN")
port = config.get("DB", "PORT")

url = f"postgresql+psycopg2://{username}:{password}@{domain}:{port}/{database_name}"
engine = create_engine(url, echo=True, pool_size=5)

DBSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# Dependency
def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()