from sqlalchemy.orm import Session
from passlib.hash import sha256_crypt
from fastapi.encoders import jsonable_encoder

from . import models, schemas


# USERS --------------------------------


def is_user_password_correct(user_password: str, password: str):
    return sha256_crypt.verify(password, user_password)


def get_user_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user


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


# GALLERIES -----------------------------
def get_gallery(db: Session, gallery_id: int):
    return db.query(models.Gallery).filter(
        models.Gallery.id == gallery_id).first()


def get_galleries(db: Session):
    return db.query(models.Gallery).order_by(models.Gallery.id).all()


def get_user_galleries(db: Session, user_id: int):
    return db.query(models.Gallery).filter(
        models.Gallery.id == user_id).order_by(models.Gallery.id).all()


def create_gallery(db: Session, gallery: schemas.Gallery):
    db_gallery = models.Gallery(**gallery.dict())
    db.add(db_gallery)
    db.commit()
    db.refresh(db_gallery)
    return db_gallery


def delete_gallery(db: Session, gallery_id: int):
    gallery = db.query(models.Gallery).filter(
        models.Gallery.id == gallery_id).first()
    if gallery:
        db.delete(gallery)
        db.commit()


def update_gallery(db: Session, gallery_id: int, gallery: schemas.Gallery):
    db_gallery = get_gallery(db, gallery_id)
    if not db_gallery:
        return NameError
    db_gallery.title = gallery.title
    db_gallery.description = gallery.description
    db_gallery.private = gallery.private
    db_gallery.image = gallery.image
    db.commit()
    db.refresh(db_gallery)
    return db_gallery
