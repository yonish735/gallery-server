import os
import jwt
from jose import JWTError
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional

from ..database import schemas

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALG")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

expired_signature = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Signature has expired",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM],
                             options={"verify_exp": True})
        username: str = payload.get("email")
        if username is None:
            raise credentials_exception
        user_id: int = payload.get("id")
        if user_id is None:
            raise credentials_exception
        return username, user_id
    except jwt.ExpiredSignatureError:
        raise expired_signature
    except JWTError:
        raise credentials_exception


def encode_token(user: schemas.User,
                 expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    return jwt.encode(
        {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "exp": expire,
        },
        JWT_SECRET,
        algorithm=ALGORITHM,
    )
