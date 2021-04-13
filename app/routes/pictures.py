from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import crud_pictures, schemas, database
from .token import oauth2_scheme, verify_token

router = APIRouter(
    tags=["picture"],
)


@router.get('/pictures/{gallery_id}/download/{picture_id}')
def download_gallery_pictures(gallery_id: int,
                              picture_id: int,
                              token: str = Depends(oauth2_scheme),
                              db: Session = Depends(database.get_db)):
    _, user_id = verify_token(token)
    return crud_pictures.download_picture(db,
                                          gallery_id=gallery_id,
                                          picture_id=picture_id,
                                          requestor_id=user_id)


@router.get('/pictures/{gallery_id}',
            response_model=Optional[List[schemas.Picture]])
def get_gallery_pictures(gallery_id: int,
                         token: str = Depends(oauth2_scheme),
                         db: Session = Depends(database.get_db)):
    verify_token(token)
    return crud_pictures.get_gallery_pictures(db, gallery_id=gallery_id)


@router.get('/pictures/public/{gallery_id}',
            response_model=Optional[List[schemas.Picture]])
def get_gallery_public_pictures(gallery_id: int,
                                token: str = Depends(oauth2_scheme),
                                db: Session = Depends(database.get_db)):
    verify_token(token)
    return crud_pictures.get_gallery_public_pictures(db, gallery_id=gallery_id)


@router.post('/pictures', response_model=schemas.Picture)
def create_picture(picture: schemas.PictureCreate,
                   token: str = Depends(oauth2_scheme),
                   db: Session = Depends(database.get_db)):
    verify_token(token)
    return crud_pictures.create_picture(db, picture=picture)


@router.delete('/pictures/{picture_id}')
def delete_gallery(picture_id: int,
                   token: str = Depends(oauth2_scheme),
                   db: Session = Depends(database.get_db)):
    verify_token(token)
    crud_pictures.delete_picture(db, picture_id)


@router.patch('/pictures/{picture_id}', response_model=schemas.Picture)
def update_gallery(picture_id: int,
                   picture: schemas.Picture,
                   token: str = Depends(oauth2_scheme),
                   db: Session = Depends(database.get_db)):
    verify_token(token)
    return crud_pictures.update_picture(db, picture_id=picture_id,
                                        picture=picture)
