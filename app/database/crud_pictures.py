from sqlalchemy.orm import Session

from . import models, schemas


# PICTURES -----------------------------


def get_gallery_pictures(db: Session, gallery_id: int):
    return db.query(models.Picture).filter(
        models.Picture.gallery_id == gallery_id).all()


def get_picture(db: Session, picture_id: int):
    return db.query(models.Picture).filter(
        models.Picture.id == picture_id).first()


def create_picture(db: Session, picture: schemas.PictureCreate):
    db_picture = models.Picture(**picture.dict())
    db.add(db_picture)
    db.commit()
    db.refresh(db_picture)
    return db_picture


def delete_picture(db: Session, picture_id: int):
    picture = db.query(models.Picture).filter(
        models.Picture.id == picture_id).first()
    if picture:
        db.delete(picture)
        db.commit()


def update_picture(db: Session, picture_id: int, picture: schemas.Picture):
    db_picture = get_picture(db, picture_id)
    if not db_picture:
        return NameError
    db_picture.title = picture.title
    db_picture.image = picture.image
    db_picture.filename = picture.filename
    db.commit()
    db.refresh(db_picture)
    return db_picture
