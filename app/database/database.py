from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

# Load environment from .env file
load_dotenv()

# Secret variables from environment
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Create session for the database
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for Models
Base = declarative_base()

# Connect to database
try:
    Base.metadata.create_all(bind=engine)
    connected = True
except:
    connected = False


def get_db():
    """
    Duplicate session
    :return: duplicated session
    """
    if not connected:
        yield None
        return
    # Duplicate session
    db = SessionLocal()
    try:
        # Yield session to caller
        yield db
    finally:
        # Close session in any case, even if caller got exception
        db.close()
