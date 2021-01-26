from sqlalchemy.orm import Session
from passlib.hash import sha256_crypt

from . import models, schemas


# USERS --------------------------------


def is_user_password_correct(user_password: str, password: str):
    return sha256_crypt.verify(password, user_password)


def get_user_by_username(db: Session, username: str, password: str):
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if user and is_user_password_correct(user.hashed_password, password):
        return user
    else:
        return None


def create_user(db: Session, user: schemas.UserCreate):
    def get_password_hash(password):
        return sha256_crypt.hash(password)

    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# GALLERIES -----------------------------
def get_galleries(db: Session):
    galleries = db.query(models.Gallery).all()
    return galleries


def create_gallery(db: Session, gallery: schemas.GalleryCreate):
    db_gallery = models.Gallery(**gallery.dict())
    db.add(db_gallery)
    db.commit()
    db.refresh(db_gallery)
    return db_gallery
