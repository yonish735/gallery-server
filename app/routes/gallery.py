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
    prefix="/galleries"
)


@router.get('', response_model=Optional[List[schemas.Gallery]])
def get_all_galleries(db: Session = Depends(database.get_db)):
    galleries = crud.get_galleries(db)
    return galleries


@router.post('', response_model=schemas.Gallery)
def create_gallery(gallery: schemas.GalleryCreate,
                   db: Session = Depends(database.get_db)):
    return crud.create_gallery(db, gallery=gallery)
