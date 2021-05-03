import os
import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional

from ..shared import schemas

# JWT token helper functions

# Secret variables from environment
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALG")

# Expect each request to have header:
# Authorization: Bearer <JWT token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Exception for wrong credentials
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# Exception for expired signature
expired_signature = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Signature has expired",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_token(token: str):
    """
    Verify validity of token
    :param token: JWT token
    :return: tuple (email, user id)
    """
    try:
        # Decode token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM],
                             options={"verify_exp": True})
        # Verify presence of email in token
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        # Verify presence of user id in token
        user_id: int = payload.get("id")
        if user_id is None:
            raise credentials_exception
        return email, user_id
    except jwt.ExpiredSignatureError:
        raise expired_signature
    except:
        raise credentials_exception


def encode_token(user: schemas.User,
                 expires_delta: Optional[timedelta] = None):
    """
    Encode JWT token
    :param user: user to encode token for
    :param expires_delta: optional expiration delta (like 7 days)
    :return: JWT token
    """
    # Calculate expiration date
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
