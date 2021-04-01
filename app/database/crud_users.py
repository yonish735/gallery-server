from sqlalchemy.orm import Session
from passlib.hash import sha256_crypt

from . import models, schemas


# USERS --------------------------------


def is_user_password_correct(user_password: str, password: str):
    return sha256_crypt.verify(password, user_password)


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_password_hash(password):
    return sha256_crypt.hash(password)


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
