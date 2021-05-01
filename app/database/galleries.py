from sqlalchemy.orm import Session
from sqlalchemy import or_, false, func

from ..shared import models, schemas


def get_gallery(db: Session, gallery_id: int):
    """
    Get gallery by id
    :param db: database session
    :param gallery_id: id of gallery
    :return: gallery
    """
    return db.query(models.Gallery).filter(
        models.Gallery.id == gallery_id).first()


def get_gallery_by_title(db: Session, title: str):
    """
    Get gallery by title
    :param db: database session
    :param title: title of gallery
    :return: gallery
    """
    return db.query(models.Gallery).filter(
        models.Gallery.title == title).first()


def get_public_galleries_by_id(db: Session, gallery_id: int):
    """
    Get public galleries that match the pattern and don't belong to user
    :param db: database session
    :param gallery_id: id of gallery
    :return: galleries
    """
    return db.query(models.Gallery) \
        .filter(models.Gallery.private == false(),
                models.Gallery.id == gallery_id).all()


def get_public_galleries_by_pattern(db: Session, pattern: str, user_id: int):
    """
    Get public galleries that match the pattern and don't belong to user
    :param db: database session
    :param pattern: pattern
    :param user_id: id of user
    :return: galleries
    """
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


def get_all_public_galleries(db: Session, user_id: int):
    """
    Get all public galleries which don't belong to user
    :param db: database session
    :param user_id: id of user
    :return: galleries
    """
    return db.query(models.Gallery) \
        .filter(models.Gallery.private == false(),
                models.Gallery.user_id != user_id) \
        .order_by(models.Gallery.title) \
        .all()


def get_public_galleries_nouser(db: Session, pattern: str):
    """
    Search by gallery id or by pattern
    :param db: database session
    :param pattern: pattern
    :return: galleries
    """
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
    """
    Search gallery titles by query
    :param db: database session
    :param q: query
    :return: titles
    """
    user_id = q.user_id
    q = q.q.lower()
    tuples = db.query(models.Gallery) \
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
    return tuples


def get_user_galleries(db: Session, user_id: int):
    """
    Get all galleries of user
    :param db: database session
    :param user_id: id of user
    :return: galleries
    """
    return db.query(models.Gallery).filter(
        models.Gallery.user_id == user_id).order_by(models.Gallery.title).all()


def create_gallery(db: Session, gallery: schemas.GalleryCreate):
    """
    Create a new gallery
    :param db: database session
    :param gallery: gallery data
    :return: new gallery
    """
    # Verify that gallery doesn't exist
    db_gallery = get_gallery_by_title(db, gallery.title)
    if db_gallery:
        return NameError
    # Convert Gallery to model
    db_gallery = models.Gallery(**gallery.dict())
    db.add(db_gallery)
    db.commit()
    # Sync gallery from database
    db.refresh(db_gallery)
    return db_gallery


def delete_gallery(db: Session, gallery_id: int):
    """
    Delete a gallery
    :param db: database session
    :param gallery_id: id of gallery
    """
    gallery = db.query(models.Gallery).filter(
        models.Gallery.id == gallery_id).first()
    if gallery:
        db.delete(gallery)
        db.commit()


def update_gallery(db: Session, gallery_id: int, gallery: schemas.Gallery):
    """
    Update a gallery
    :param db: database session
    :param gallery_id: id of gallery
    :param gallery: gallery data
    :return: gallery
    """
    # Find gallery
    db_gallery = get_gallery(db, gallery_id)
    if not db_gallery:
        return NameError
    # Update data
    db_gallery.title = gallery.title
    db_gallery.description = gallery.description
    db_gallery.private = gallery.private
    db_gallery.image = gallery.image
    db_gallery.filename = gallery.filename
    db.commit()
    # Sync gallery from database
    db.refresh(db_gallery)
    return db_gallery
