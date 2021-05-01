import secrets

from sqlalchemy.orm import Session
from passlib.hash import sha256_crypt

from ..shared import models, schemas


def is_user_password_correct(user_password: str, password: str):
    """
    Helper for verification of password correction
    :param user_password: encoded password from DB
    :param password: supplied password by user during login
    :return: true or false
    """
    return sha256_crypt.verify(password, user_password)


def get_password_hash(password):
    """
    Helper to hash password
    :param password: password to hash
    :return: hashed password
    """
    return sha256_crypt.hash(password)


def get_user_by_email(db: Session, email: str):
    """
    Get user by email
    :param db: database session
    :param email: user's email
    :return: user
    """
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    """
    Create user
    :param db: database session
    :param user: user data
    :param hashed_password: hashed password
    :return: new user
    """
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    # Sync user from database
    db.refresh(db_user)
    return db_user


def update_password(db: Session, user: schemas.UserForgotPassword,
                    hashed_password: str):
    """
    Update users password
    :param db: database session
    :param user: user data
    :param hashed_password: hashed password
    :return: updated user
    """
    # find user by email
    db_user = get_user_by_email(db, email=user.email)
    # Update password
    db_user.hashed_password = hashed_password
    db.commit()
    # Sync user from database
    db.refresh(db_user)
    return db_user


def generate_token(db: Session, email: str):
    """
    Generate token for password restoration
    :param db: database session
    :param email: email of user
    :return: token
    """
    # find user by email
    db_user = get_user_by_email(db, email=email)
    if not db_user:
        return None
    # Generate token
    token = secrets.token_hex(16)
    # Store token in DB
    db_user.token = token
    db.commit()
    return token


def download_requests(db: Session, user_id: str):
    """
    Get list of download requests for user
    :param db: database session
    :param user_id: id of user
    :return: list of requests
    """
    requests = db.query(models.Download).filter(
        models.Download.owner_id == user_id).all()
    return requests


def download_find(db: Session, req_id: str, user_id: str):
    """
    Get specific download request
    :param db: database session
    :param req_id: request id
    :param user_id: user id
    :return: request
    """
    request = db.query(models.Download).filter(
        models.Download.owner_id == user_id,
        models.Download.id == req_id).first()
    if not request:
        return None
    return request


def download_delete(db: Session, req_id: str):
    """
    Delete download request
    :param db: database session
    :param req_id: request id
    """
    db.query(models.Download).filter_by(id=req_id).delete()
    db.commit()


def download_delete_picture(db: Session, picture_id: str):
    """
    Delete download request in case picture was deleted
    :param db: database session
    :param picture_id: picture id
    """
    db.query(models.Download).filter_by(picture_id=picture_id).delete()
    db.commit()
