import os
import re
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

import jwt

from ..database import crud_users, schemas, database

JWT_SECRET = os.getenv("JWT_SECRET")

# Format of password and email
pwd_re = re.compile(r'^\w{6,}$')
email_re = re.compile(r'^\w+@[a-zA-Z0-9_.]+$')

router = APIRouter(
    tags=["users"],
    prefix="/users"
)


def encode(user: schemas.User):
    expire = datetime.utcnow() + timedelta(minutes=15)
    return jwt.encode(
        {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "exp": expire,
        },
        JWT_SECRET,
        algorithm="HS256",
    )


@router.post("/signUp", response_model=schemas.TokenResponse)
def register(user: schemas.UserCreate,
             db: Session = Depends(database.get_db)):
    db_user = crud_users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="User already exists")
    if not pwd_re.match(user.password):
        raise HTTPException(status_code=400,
                            detail="Password should be at lease six numbers"
                                   " and letters")
    if not email_re.match(user.email):
        raise HTTPException(status_code=400,
                            detail="Invalid email")

    hashed_password = crud_users.get_password_hash(user.password)
    db_user = crud_users.create_user(db=db, user=user,
                                     hashed_password=hashed_password)
    if not db_user:
        raise HTTPException(status_code=500, detail="Something went wrong")

    try:
        encoded_jwt = encode(db_user)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return {
        "token": encoded_jwt,
    }


@router.post("/signIn", response_model=schemas.TokenResponse)
def signin(user: schemas.UserLogin,
           db: Session = Depends(database.get_db)):
    db_user = crud_users.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User doesn't exist")

    is_password_correct = crud_users.is_user_password_correct(
        db_user.hashed_password, user.password)
    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    try:
        encoded_jwt = encode(db_user)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return {
        "token": encoded_jwt,
    }


@router.post("/forgot", response_model=schemas.TokenResponse)
def forgot(user: schemas.UserForgotPassword,
           db: Session = Depends(database.get_db)):
    db_user = crud_users.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    if db_user.token != user.token:
        raise HTTPException(status_code=400, detail="Invalid token")
    hashed_password = crud_users.get_password_hash(user.password)
    db_user = crud_users.update_password(db=db, user=user,
                                         hashed_password=hashed_password)
    if not db_user:
        raise HTTPException(status_code=500, detail="Something went wrong")

    try:
        encoded_jwt = encode(db_user)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return {
        "token": encoded_jwt,
    }


@router.get("/sendToken/{email}")
def send_token(email: str, db: Session = Depends(database.get_db)):
    token = crud_users.generate_token(db, email=email)
    if token is not None:
        # TODO: send token
        print(token)
    # hide problems
    return {"ok": True}
