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


@router.get('/{user_id}',
            response_model=Optional[List[schemas.Gallery]])
def get_user_galleries(user_id: int,
                       token: str = Depends(oauth2_scheme),
                       db: Session = Depends(database.get_db)):
    """
    Get galleries of the user
    :param user_id: user id
    :param token: JWT token
    :param db: database session
    :return: galleries
    """
    # Verify that user is logged in
    verify_token(token)
    return galleries.get_user_galleries(db, user_id=user_id)


@router.get('/public_all/{user_id}',
            response_model=Optional[List[schemas.GalleryWithUser]])
def get_public_galleries_all(
        user_id: int,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(database.get_db)):
    """
    Get all public galleries of user
    :param user_id: id of user
    :param token: JWT token
    :param db: database session
    :return: galleries
    """
    # Verify that user is logged in
    _, _id = verify_token(token)
    # Use current user's id if user id not supplied
    if user_id == 0:
        user_id = _id
    if user_id != 0:
        return galleries.get_all_public_galleries(db, user_id=user_id)
    return []


@router.get('/public/g/{gallery_id}',
            response_model=Optional[List[schemas.GalleryWithUser]])
def get_public_galleries_by_id(gallery_id: int,
                               token: str = Depends(oauth2_scheme),
                               db: Session = Depends(database.get_db)):
    """
    Get public galleries for a user according to gallery id
    :param gallery_id: id of gallery
    :param token: JWT token
    :param db: database session
    :return: galleries
    """
    # Verify that user is logged in
    _, _id = verify_token(token)
    return galleries.get_public_galleries_by_id(db, gallery_id=gallery_id)


@router.get('/public/{user_id}/p/{pattern}',
            response_model=Optional[List[schemas.GalleryWithUser]])
def get_public_galleries(pattern: str,
                         user_id: int,
                         token: str = Depends(oauth2_scheme),
                         db: Session = Depends(database.get_db)):
    """
    Get public galleries for a user according to pattern or gallery id
    :param pattern: pattern to search for
    :param user_id: id of user
    :param token: JWT token
    :param db: database session
    :return: galleries
    """
    # Verify that user is logged in
    _, _id = verify_token(token)
    # Use current user's id if user id not supplied
    if user_id == 0:
        user_id = _id
    if user_id != 0:
        # if user is defined return public galleries of the user
        return galleries.get_public_galleries_by_pattern(db, pattern=pattern, user_id=user_id)
    else:
        # otherwise return public galleries of all users
        return galleries.get_public_galleries_nouser(db, pattern=pattern)


@router.get('/public/{user_id}',
            response_model=Optional[List[schemas.Gallery]])
def get_public_galleries_no_pattern(user_id: int,
                                    token: str = Depends(oauth2_scheme),
                                    db: Session = Depends(database.get_db)):
    """
    Get public galleries without using pattern
    :param user_id: id of user
    :param token: JWT token
    :param db: database session
    :return: galleries
    """
    # Verify that user is logged in
    verify_token(token)
    return galleries.get_public_galleries(db, pattern='',
                                          user_id=user_id)


def map_suggestion(s):
    """
    Helper function to map tuple to dictionary
    :param s: tuple of id and text
    :return: dictionary with keys id and text
    """
    return {
        'id': s[0],
        'text': s[1],
    }


@router.post('/suggestions', response_model=schemas.Suggestion)
def suggest_galleries(q: Optional[schemas.Query] = None,
                      token: str = Depends(oauth2_scheme),
                      db: Session = Depends(database.get_db)):
    """
    Get suggestions for galleries
    :param q: query
    :param token: JWT token
    :param db: database session
    :return: suggestions
    """
    # Verify that user is logged in
    verify_token(token)
    suggestions = []
    if q is not None:
        # get title of galleries that match the query
        # suggestion has two parts, title and id
        tuples = galleries.search_gallery_titles(db, q=q)
        for t in tuples:
            suggestions.append((t[0], t[1]))
    return {
        'suggestions': suggestions,
    }


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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to find this gallery")
    return gallery
