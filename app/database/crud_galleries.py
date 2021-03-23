from sqlalchemy.orm import Session
from sqlalchemy import or_, false

from . import models, schemas


# GALLERIES -----------------------------


def get_gallery(db: Session, gallery_id: int):
    return db.query(models.Gallery).filter(
        models.Gallery.id == gallery_id).first()


def get_public_galleries(db: Session, pattern: str, user_id: int):
    pattern = pattern.lower()
    galleries = db.query(models.Gallery) \
        .filter(models.Gallery.private == false(),
                or_(models.Gallery.title.ilike(f'%{pattern}%'),
                    models.Gallery.description.ilike(f'%{pattern}%'))) \
        .filter(models.Gallery.user_id != user_id) \
        .order_by(models.Gallery.title) \
        .all()
    if galleries is None:
        galleries = db.query(models.Gallery) \
            .filter(models.Gallery.private == false(),
                    (models.Gallery.title + ": " + models.Gallery.description).
                    contains(pattern),
                    ) \
            .filter(models.Gallery.user_id != user_id) \
            .order_by(models.Gallery.title) \
            .all()
    return galleries


def search_gallery_titles(db: Session, q: schemas.Query):
    user_id = q.user_id
    q = q.q.lower()
    titles = db.query(models.Gallery) \
        .with_entities(models.Gallery.title + ": " +
                       models.Gallery.description) \
        .filter(
        or_(
            models.Gallery.title.contains(q),
            models.Gallery.description.contains(q)
        )
    ) \
        .filter(models.Gallery.private is not True) \
        .filter(models.Gallery.user_id != user_id) \
        .order_by(models.Gallery.title) \
        .all()
    if titles is None:
        titles = db.query(models.Gallery) \
            .with_entities(models.Gallery.title + ": " +
                           models.Gallery.description) \
            .filter(
            (models.Gallery.title + ": " + models.Gallery.description).
                contains(q),
        ) \
            .filter(models.Gallery.private is not True) \
            .filter(models.Gallery.user_id != user_id) \
            .order_by(models.Gallery.title) \
            .all()

    return titles


def get_user_galleries(db: Session, user_id: int):
    return db.query(models.Gallery).filter(
        models.Gallery.user_id == user_id).order_by(models.Gallery.id).all()


def create_gallery(db: Session, gallery: schemas.GalleryCreate):
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
    db_gallery.filename = gallery.filename
    db.commit()
    db.refresh(db_gallery)
    return db_gallery
