from sqlalchemy.orm import Session
from sqlalchemy import or_, false, func

from . import models, schemas


# GALLERIES -----------------------------


def get_gallery(db: Session, gallery_id: int):
    return db.query(models.Gallery).filter(
        models.Gallery.id == gallery_id).first()


def get_public_galleries(db: Session, pattern: str, gallery_id: int,
                         user_id: int):
    if gallery_id is not None and gallery_id != 0:
        return db.query(models.Gallery) \
            .filter(models.Gallery.private == false(),
                    models.Gallery.id == gallery_id).all()

    pattern = pattern.lower()
    galleries = db.query(models.Gallery) \
        .filter(models.Gallery.private == false(),
                models.Gallery.user_id != user_id,
                or_(
                    or_(models.Gallery.title.ilike(f'%{pattern}%'),
                        models.Gallery.description.ilike(f'%{pattern}%')),
                    func.lower((models.Gallery.title + ": " +
                                models.Gallery.description)) == pattern
                ),
                ) \
        .order_by(models.Gallery.title) \
        .all()
    return galleries


def get_public_galleries_nouser(db: Session, pattern: str, gallery_id: int):
    if gallery_id is not None and gallery_id != 0:
        return db.query(models.Gallery) \
            .filter(models.Gallery.private == false(),
                    models.Gallery.id == gallery_id).all()

    pattern = pattern.lower()
    galleries = db.query(models.Gallery) \
        .filter(models.Gallery.private == false(),
                or_(
                    or_(models.Gallery.title.ilike(f'%{pattern}%'),
                        models.Gallery.description.ilike(f'%{pattern}%')),
                    func.lower((models.Gallery.title + ": " +
                                models.Gallery.description)) == pattern
                ),
                ) \
        .order_by(models.Gallery.title) \
        .all()
    return galleries


def search_gallery_titles(db: Session, q: schemas.Query):
    user_id = q.user_id
    q = q.q.lower()
    titles = db.query(models.Gallery) \
        .with_entities(models.Gallery.title + ": " +
                       models.Gallery.description,
                       models.Gallery.id) \
        .filter(
        models.Gallery.private == false(),
        models.Gallery.user_id != user_id,
        or_(
            or_(
                models.Gallery.title.contains(q),
                models.Gallery.description.contains(q)
            ),
            (models.Gallery.title + ": " +
             models.Gallery.description).contains(q)
        )
    ) \
        .order_by(models.Gallery.title) \
        .all()
    return titles


def get_public_gallery(db: Session, gallery_id: int):
    return db.query(models.Gallery) \
        .filter(
        models.Gallery.private == false(),
        models.Gallery.id == gallery_id
    ).all()


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
