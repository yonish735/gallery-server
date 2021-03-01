import io
from typing import List, Optional

from PIL import Image
from fastapi import APIRouter, Cookie, Form, status, UploadFile, File, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from starlette.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..database import crud, schemas, database

router = APIRouter(
    tags=["gallery"],
)


@router.get('/galleries', response_model=Optional[List[schemas.Gallery]])
def get_all_galleries(db: Session = Depends(database.get_db)):
    galleries = crud.get_galleries(db)
    return galleries


@router.get('/galleries/{user_id}',
            response_model=Optional[List[schemas.Gallery]])
def get_user_galleries(user_id: int, db: Session = Depends(database.get_db)):
    galleries = crud.get_user_galleries(db, user_id=user_id)
    return galleries


@router.post('/galleries', response_model=schemas.Gallery)
def create_gallery(gallery: schemas.GalleryCreate,
                   db: Session = Depends(database.get_db)):
    return crud.create_gallery(db, gallery=gallery)


@router.delete('/galleries/{gallery_id}')
def delete_gallery(gallery_id: int, db: Session = Depends(database.get_db)):
    crud.delete_gallery(db, gallery_id)


@router.patch('/galleries/{gallery_id}', response_model=schemas.Gallery)
def update_gallery(gallery_id: int, gallery: schemas.Gallery,
                   db: Session = Depends(database.get_db)):
    return crud.update_gallery(db, gallery_id, gallery)
