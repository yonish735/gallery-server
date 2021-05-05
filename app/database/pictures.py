from sqlalchemy.orm import Session
from sqlalchemy import false
from datetime import datetime

from ..shared import models, schemas
from .users import download_delete_picture


def download_picture(db: Session, picture_id: int, requestor_id: int):
    """
    Create request to download picture
    :param db: database session
    :param picture_id: picture id
    :param requestor_id: requestor id
    :return: id of picture
    """
    # Verify the picture exists
    picture = db.query(models.Picture).filter(
        models.Picture.id == picture_id).first()
    if picture is None:
        return {"download": False}
    # Create download request
    download = {
        "requestor_id": requestor_id,
        "owner_id": picture.gallery.user_id,
        "gallery_id": picture.gallery.id,
        "picture_id": picture_id,
        "created_at": datetime.utcnow(),
    }
    # Convert request to model
    db_download = models.Download(**download)
    db.add(db_download)
    db.commit()
    return {"pictureId": picture_id}


def get_gallery_pictures(db: Session, gallery_id: int):
    """
    Get all pictures from gallery
    :param db: database session
    :param gallery_id: id of gallery
    :return: pictures
    """
    return db.query(models.Picture).filter(
        models.Picture.gallery_id == gallery_id).all()


def get_gallery_public_pictures(db: Session, gallery_id: int):
    """
    Get public pictures from gallery
    :param db: database session
    :param gallery_id: gallery id
    :return: pictures
    """
    return db.query(models.Picture).filter(
        models.Gallery.private == false(),
        models.Picture.private == false(),
        models.Picture.gallery_id == gallery_id).all()


def get_picture(db: Session, picture_id: int):
    """
    Get picture by id
    :param db: database session
    :param picture_id: picture id
    :return: picture
    """
    return db.query(models.Picture).filter(
        models.Picture.id == picture_id).first()


def create_picture(db: Session, picture: schemas.PictureCreate):
    """
    Create a new picture
    :param db: database session
    :param picture: picture data
    :return: picture
    """
    # Convert picture to model
    db_picture = models.Picture(**picture.dict())
    db.add(db_picture)
    db.commit()
    # Sync picture from database
    db.refresh(db_picture)
    return db_picture


def delete_picture(db: Session, picture_id: int):
    """
    Delete a picture
    :param db: database session
    :param picture_id: picture id
    """
    picture = db.query(models.Picture).filter(
        models.Picture.id == picture_id).first()
    if picture:
        download_delete_picture(db, picture_id=picture_id)
        db.delete(picture)
        db.commit()


def update_picture(db: Session, picture_id: int, picture: schemas.Picture):
    """
    Update picture data
    :param db: database session
    :param picture_id: picture id
    :param picture: picture data
    :return: updated picture
    """
    # Find picture
    db_picture = get_picture(db, picture_id)
    if not db_picture:
        return NameError
    # Update data
    db_picture.title = picture.title
    db_picture.description = picture.description
    db_picture.image = picture.image
    db_picture.filename = picture.filename
    db_picture.private = picture.private
    db.commit()
    # Sync picture from database
    db.refresh(db_picture)
    return db_picture
