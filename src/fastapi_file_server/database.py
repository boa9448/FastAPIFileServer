from sqlalchemy import event, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

from fastapi_file_server.config import get_config


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


config = get_config()
engin = create_engine(config.database_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engin)
Base = declarative_base()


def create_db():
    Base.metadata.create_all(bind=engin)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()