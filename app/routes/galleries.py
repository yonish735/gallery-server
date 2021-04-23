from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import crud_galleries, schemas, database
from .token import oauth2_scheme, verify_token

router = APIRouter(
    tags=["gallery"],
)


@router.get('/galleries/{user_id}',
            response_model=Optional[List[schemas.Gallery]])
def get_user_galleries(user_id: int,
                       token: str = Depends(oauth2_scheme),
                       db: Session = Depends(database.get_db)):
    verify_token(token)
    return crud_galleries.get_user_galleries(db, user_id=user_id)


@router.get('/galleries/public_all/{user_id}',
            response_model=Optional[List[schemas.GalleryWithUser]])
def get_public_galleries_all(
        user_id: int,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(database.get_db)):
    _, _id = verify_token(token)
    if user_id == 0:
        user_id = _id
    if user_id != 0:
        return crud_galleries.get_all_public_galleries(db, user_id=user_id)
    return []


@router.get('/galleries/public/{user_id}/{pattern}/{gallery_id}',
            response_model=Optional[List[schemas.GalleryWithUser]])
def get_public_galleries(pattern: str,
                         gallery_id: int,
                         user_id: int,
                         token: str = Depends(oauth2_scheme),
                         db: Session = Depends(database.get_db)):
    _, _id = verify_token(token)
    if user_id == 0:
        user_id = _id
    if user_id != 0:
        return crud_galleries.get_public_galleries(db, pattern=pattern,
                                                   gallery_id=gallery_id,
                                                   user_id=user_id)
    else:
        return crud_galleries.get_public_galleries_nouser(
            db,
            pattern=pattern,
            gallery_id=gallery_id)


@router.get('/galleries/public/one/{gallery_id}',
            response_model=Optional[List[schemas.GalleryWithUser]])
def get_public_gallery(gallery_id: int,
                       token: str = Depends(oauth2_scheme),
                       db: Session = Depends(database.get_db)):
    verify_token(token)
    return crud_galleries.get_public_gallery(db, gallery_id=gallery_id)


@router.get('/galleries/public/{user_id}',
            response_model=Optional[List[schemas.Gallery]])
def get_public_galleries_no_pattern(user_id: int,
                                    token: str = Depends(oauth2_scheme),
                                    db: Session = Depends(database.get_db)):
    verify_token(token)
    return crud_galleries.get_public_galleries(db, pattern='',
                                               user_id=user_id)


def map_suggestion(s: tuple[str, int]):
    return {
        'id': s[0],
        'text': s[1],
    }


@router.post('/galleries/suggestions', response_model=schemas.Suggestion)
def search_galleries(q: Optional[schemas.Query] = None,
                     db: Session = Depends(database.get_db)):
    suggestions = []
    if q is not None:
        titles = crud_galleries.search_gallery_titles(db, q=q)
        for t in titles:
            suggestions.append((t[0], t[1]))
    return {
        'suggestions': suggestions,
    }


@router.post('/galleries', response_model=schemas.Gallery)
def create_gallery(gallery: schemas.GalleryCreate,
                   token: str = Depends(oauth2_scheme),
                   db: Session = Depends(database.get_db)):
    verify_token(token)
    gallery = crud_galleries.create_gallery(db, gallery=gallery)
    if gallery == NameError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Gallery with the same title already exists")
    return gallery


@router.delete('/galleries/{gallery_id}', response_model=str)
def delete_gallery(gallery_id: int,
                   token: str = Depends(oauth2_scheme),
                   db: Session = Depends(database.get_db)):
    verify_token(token)
    crud_galleries.delete_gallery(db, gallery_id)
    return gallery_id


@router.patch('/galleries/{gallery_id}', response_model=schemas.Gallery)
def update_gallery(gallery_id: int, gallery: schemas.Gallery,
                   token: str = Depends(oauth2_scheme),
                   db: Session = Depends(database.get_db)):
    verify_token(token)
    gallery = crud_galleries.update_gallery(db, gallery_id=gallery_id,
                                            gallery=gallery)
    if gallery == NameError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to find this gallery")
    return gallery
