from typing import Optional

from fastapi import APIRouter, Form, status, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.orm import Session

from ..database import crud, schemas, database

router = APIRouter(
    tags=["users"],
    prefix="/users"
)


@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate,
             db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username,
                                        password=user.password)
    if db_user:
        raise HTTPException(status_code=400,
                            detail="Username is already registered")
    else:
        return crud.create_user(db=db, user=user)


@router.post("/login", response_model=schemas.User)
def login(username: str,
          password: str,
          db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username=username,
                                        password=password)
    if db_user:
        return db_user
    else:
        raise HTTPException(status_code=400, detail="Unable to find user")
