import re
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import users, database
from .token import encode_token, oauth2_scheme, verify_token

from ..shared import email as smtp, schemas

# Format of password and email
pwd_re = re.compile(r'^\w{6,}$')
email_re = re.compile(r'^\w+@[a-zA-Z0-9_.]+$')

# Initialization of router /users
router = APIRouter(
    tags=["users"],
    prefix="/users"
)


@router.post("/signUp", response_model=schemas.TokenResponse)
def register(user: schemas.UserCreate,
             db: Session = Depends(database.get_db)):
    """
    Registration of a new user
    :param user: user data to create
    :param db: database session
    :return: JWT token
    """
    # Check that user doesn't exist
    db_user = users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="User already exists")
    # Check validity of password
    if not pwd_re.match(user.password):
        raise HTTPException(status_code=400,
                            detail="Password should be at least six numbers"
                                   " and letters")
    # Check validity of email
    if not email_re.match(user.email):
        raise HTTPException(status_code=400,
                            detail="Invalid email")

    # Hash password and create user
    hashed_password = users.get_password_hash(user.password)
    db_user = users.create_user(db=db, user=user,
                                hashed_password=hashed_password)
    if not db_user:
        raise HTTPException(status_code=500, detail="Something went wrong")

    try:
        # Create JWT token
        encoded_jwt = encode_token(db_user)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return {
        "token": encoded_jwt,
    }


@router.post("/signIn", response_model=schemas.TokenResponse)
def signin(user: schemas.UserLogin,
           db: Session = Depends(database.get_db)):
    """
    Log user in
    :param user: user data to login
    :param db: database session
    :return: JWT token
    """
    # Fetch user from DB
    db_user = users.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="Invalid credentials")

    # Validate password
    is_password_correct = users.is_user_password_correct(
        db_user.hashed_password, user.password)
    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    encoded_jwt = encode_token(db_user)
    try:
        # Create JWT token
        encoded_jwt = encode_token(db_user)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return {
        "token": encoded_jwt,
    }


@router.post("/forgot", response_model=schemas.TokenResponse)
def forgot(user: schemas.UserForgotPassword,
           db: Session = Depends(database.get_db)):
    """
    Update user that forgot password
    :param user: user that forgot password
    :param db: database session
    :return: JWT token
    """
    # Fetch user from DB
    db_user = users.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    # Validate token
    if db_user.token != user.token:
        raise HTTPException(status_code=400, detail="Invalid token")
    # Hash password and update it for user
    hashed_password = users.get_password_hash(user.password)
    db_user = users.update_password(db=db, user=user,
                                    hashed_password=hashed_password)
    if not db_user:
        raise HTTPException(status_code=500, detail="Something went wrong")

    try:
        # Create JWT token
        encoded_jwt = encode_token(db_user)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return {
        "token": encoded_jwt,
    }


@router.get("/sendToken/{email}")
def send_token(email: str, db: Session = Depends(database.get_db)):
    """
    Send token via email
    :param email: email to send token to
    :param db: database session
    :return: simulate success
    """
    # Generate token
    token = users.generate_token(db, email=email)
    if token is not None and email != "":
        # Send it
        smtp.send_token(email, token)
    # Hide problems
    return {"ok": True}


@router.get("/download", response_model=List[schemas.Download])
def get_download_requests(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(database.get_db)):
    """
    Fetches list of download request for current user
    :param token: JWT token
    :param db: database session
    :return: list of download requests
    """
    # Verify that user is logged in
    _, user_id = verify_token(token)
    # Fetch list of requests from DB
    return users.download_requests(db, user_id=user_id)


@router.get("/download/permit/{req_id}/{permit}")
def permit_download_request(
        req_id: str,
        permit: str,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(database.get_db)):
    """
    Permit download request and send email with picture
    :param req_id: id of download request
    :param permit: true or false
    :param token: JWT token
    :param db: database session
    :return: simulate success
    """
    # Verify that user is logged in
    email, user_id = verify_token(token)
    # Fetch user from DB
    user = users.get_user_by_email(db, email)
    # Fetch download request from DB
    request = users.download_find(db, req_id=req_id, user_id=user_id)
    # If everything is OK then send picture
    if user is not None and request is not None and permit == 'true':
        smtp.send_picture(request, user)
    # Delete download request from DB
    users.download_delete(db, req_id=req_id)
    # Hide problems
    return {"ok": True}
