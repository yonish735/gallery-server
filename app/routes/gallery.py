import io
from typing import List, Optional

from PIL import Image
from fastapi import APIRouter, Cookie, Form, status, UploadFile, File, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from starlette.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..database import crud_galleries, schemas, database

router = APIRouter(
    tags=["gallery"],
)


@router.get('/galleries/{user_id}',
            response_model=Optional[List[schemas.Gallery]])
def get_user_galleries(user_id: int, db: Session = Depends(database.get_db)):
    return crud_galleries.get_user_galleries(db, user_id=user_id)


@router.get('/galleries/public/{pattern}',
            response_model=Optional[List[schemas.Gallery]])
def get_public_galleries(pattern: str,
                         db: Session = Depends(database.get_db)):
    return crud_galleries.get_public_galleries(db, pattern=pattern)


@router.post('/galleries/suggestions/')
def search_gallery(q: Optional[schemas.Query] = None,
                   db: Session = Depends(database.get_db)):
    if q is None:
        return []
    return crud_galleries.search_gallery_titles(db, q=q)


@router.post('/galleries', response_model=schemas.Gallery)
def create_gallery(gallery: schemas.GalleryCreate,
                   db: Session = Depends(database.get_db)):
    return crud_galleries.create_gallery(db, gallery=gallery)


@router.delete('/galleries/{gallery_id}')
def delete_gallery(gallery_id: int, db: Session = Depends(database.get_db)):
    crud_galleries.delete_gallery(db, gallery_id)


@router.patch('/galleries/{gallery_id}', response_model=schemas.Gallery)
def update_gallery(gallery_id: int, gallery: schemas.Gallery,
                   db: Session = Depends(database.get_db)):
    return crud_galleries.update_gallery(db, gallery_id=gallery_id,
                                         gallery=gallery)
