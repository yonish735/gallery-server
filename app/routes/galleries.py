from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from ..database import crud_galleries, schemas, database
from .users import JWT_SECRET, ALGORITHM, oauth2_scheme

router = APIRouter(
    tags=["gallery"],
)


@router.get('/galleries/{user_id}',
            response_model=Optional[List[schemas.Gallery]])
def get_user_galleries(user_id: int,
                       token: str = Depends(oauth2_scheme),
                       db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("email")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
        # TODO: check user_id
    except JWTError:
        raise credentials_exception

    return crud_galleries.get_user_galleries(db, user_id=user_id)


@router.get('/galleries/public/{user_id}/{pattern}/{gallery_id}',
            response_model=Optional[List[schemas.Gallery]])
def get_public_galleries(pattern: str,
                         gallery_id: int,
                         user_id: int,
                         db: Session = Depends(database.get_db)):
    if user_id != 0:
        return crud_galleries.get_public_galleries(db, pattern=pattern,
                                                   gallery_id=gallery_id,
                                                   user_id=user_id)
    else:
        return crud_galleries.get_public_galleries_nouser(db, pattern=pattern,
                                                   gallery_id=gallery_id)



@router.get('/galleries/public/one/{gallery_id}',
            response_model=Optional[List[schemas.Gallery]])
def get_public_gallery(gallery_id: int,
                       db: Session = Depends(database.get_db)):
    return crud_galleries.get_public_gallery(db, gallery_id=gallery_id)


@router.get('/galleries/public/{user_id}',
            response_model=Optional[List[schemas.Gallery]])
def get_public_galleries_no_pattern(user_id: int,
                                    db: Session = Depends(database.get_db)):
    return crud_galleries.get_public_galleries(db, pattern='',
                                               user_id=user_id)


@router.post('/galleries/suggestions')
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
