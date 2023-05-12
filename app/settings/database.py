from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
# from app.config import settings
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# production SQLALCHEMY_DATABASE_URI = f'postgresql://{settings.database_username}:{settings.database_password}@{
# settings.database_hostname}

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)
