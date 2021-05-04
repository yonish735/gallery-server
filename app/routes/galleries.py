from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import galleries, database
from ..shared import schemas
from .token import oauth2_scheme, verify_token

# Initialization of router /galleries
router = APIRouter(
    tags=["gallery"],
    prefix="/galleries"
)


@router.get('/',
            response_model=Optional[List[schemas.Gallery]])
def get_user_galleries(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(database.get_db)):
    """
    Get galleries of the user
    :param token: JWT token
    :param db: database session
    :return: galleries
    """
    # Verify that user is logged in
    _, user_id = verify_token(token)
    return galleries.get_user_galleries(db, user_id=user_id)


@router.get('/public',
            response_model=Optional[List[schemas.GalleryWithUser]])
def get_public_galleries(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(database.get_db)):
    """
    Get all public galleries of user
    :param token: JWT token
    :param db: database session
    :return: galleries
    """
    # Verify that user is logged in
    _, user_id = verify_token(token)
    if user_id != 0:
        return galleries.get_public_galleries(db, user_id=user_id)
    return []


@router.post('/', response_model=schemas.Gallery)
def create_gallery(gallery: schemas.GalleryCreate,
                   token: str = Depends(oauth2_scheme),
                   db: Session = Depends(database.get_db)):
    """
    Create a gallery
    :param gallery: gallery data
    :param token: JWT token
    :param db: database session
    :return: new gallery
    """
    # Verify that user is logged in
    verify_token(token)
    gallery = galleries.create_gallery(db, gallery=gallery)
    if gallery == NameError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Gallery with the same title already exists")
    return gallery


@router.delete('/{gallery_id}', response_model=str)
def delete_gallery(gallery_id: int,
                   token: str = Depends(oauth2_scheme),
                   db: Session = Depends(database.get_db)):
    """
    Delete the gallery
    :param gallery_id: id of gallery
    :param token: JWT token
    :param db: database session:
    :return: gallery id
    """
    # Verify that user is logged in
    verify_token(token)
    galleries.delete_gallery(db, gallery_id)
    return gallery_id


@router.patch('/{gallery_id}', response_model=schemas.Gallery)
def update_gallery(gallery_id: int, gallery: schemas.Gallery,
                   token: str = Depends(oauth2_scheme),
                   db: Session = Depends(database.get_db)):
    """
    Update a gallery
    :param gallery_id: id of gallery
    :param gallery: new data
    :param token: JWT token
    :param db: database session
    :return: updated gallery
    """
    # Verify that user is logged in
    verify_token(token)
    gallery = galleries.update_gallery(db, gallery_id=gallery_id,
                                       gallery=gallery)
    if gallery == NameError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Gallery with the same title already exists")

    if gallery == NotImplementedError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to find this gallery")
    return gallery
