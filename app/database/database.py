from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for Models
Base = declarative_base()

try:
    Base.metadata.create_all(bind=engine)
    connected = True
except:
    connected = False


def get_db():
    if not connected:
        yield None
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
