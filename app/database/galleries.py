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


def get_public_galleries(db: Session, user_id: int):
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
    # Verify that another gallery with the same title doesn't exist
    db_gallery_title = get_gallery_by_title(db, gallery.title)
    if db_gallery_title is not None and db_gallery_title.id != gallery_id:
        return NameError
    # Find gallery
    db_gallery = get_gallery(db, gallery_id)
    if not db_gallery:
        return NotImplementedError
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
