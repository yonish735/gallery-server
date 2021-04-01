import io
from typing import List, Optional

from PIL import Image
from fastapi import APIRouter, Cookie, Form, status, UploadFile, File, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from starlette.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..database import crud_pictures, schemas, database

router = APIRouter(
    tags=["picture"],
)


# TODO rename like to download
@router.get('/pictures/{gallery_id}/like/{picture_id}/user/{requestor_id}')
def like_gallery_pictures(gallery_id: int,
                          picture_id: int,
                          requestor_id: int,
                          db: Session = Depends(database.get_db)):
    return crud_pictures.like_picture(db,
                                      gallery_id=gallery_id,
                                      picture_id=picture_id,
                                      requestor_id=requestor_id)


@router.get('/pictures/{gallery_id}',
            response_model=Optional[List[schemas.Picture]])
def get_gallery_pictures(gallery_id: int,
                         db: Session = Depends(database.get_db)):
    return crud_pictures.get_gallery_pictures(db, gallery_id=gallery_id)


@router.get('/pictures/public/{gallery_id}',
            response_model=Optional[List[schemas.Picture]])
def get_gallery_public_pictures(gallery_id: int,
                                db: Session = Depends(database.get_db)):
    return crud_pictures.get_gallery_public_pictures(db, gallery_id=gallery_id)


@router.post('/pictures', response_model=schemas.Picture)
def create_picture(picture: schemas.PictureCreate,
                   db: Session = Depends(database.get_db)):
    return crud_pictures.create_picture(db, picture=picture)


@router.delete('/pictures/{picture_id}')
def delete_gallery(picture_id: int, db: Session = Depends(database.get_db)):
    crud_pictures.delete_picture(db, picture_id)


@router.patch('/pictures/{picture_id}', response_model=schemas.Picture)
def update_gallery(picture_id: int, picture: schemas.Picture,
                   db: Session = Depends(database.get_db)):
    return crud_pictures.update_picture(db, picture_id=picture_id,
                                        picture=picture)
