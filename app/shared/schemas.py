from typing import List, Optional, Tuple
from datetime import datetime
from pydantic import BaseModel


# Presentation of different types in system
# Loosely related to models


# Base Gallery class
class GalleryBase(BaseModel):
    title: str
    description: str
    private: bool
    image: Optional[str] = None
    filename: Optional[str] = None


# Gallery before creation (it has user id)
class GalleryCreate(GalleryBase):
    user_id: int


# Gallery after creation (it has id)
class Gallery(GalleryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# Base Picture class
class PictureBase(BaseModel):
    title: str
    description: str
    private: bool
    image: Optional[str] = None
    filename: Optional[str] = None


# Picture before creation (it has gallery id)
class PictureCreate(PictureBase):
    gallery_id: int


# Picture after creation (it has id)
class Picture(PictureBase):
    id: int
    gallery_id: int

    class Config:
        orm_mode = True


# Base User class
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


# Login data
class UserLogin(BaseModel):
    email: str
    password: str


# User before creation (it has password)
class UserCreate(UserBase):
    password: str


# Update password for user (via forgot password)
class UserForgotPassword(BaseModel):
    email: str
    password: str
    token: str


# User after creation (it has id and galleries)
class User(UserBase):
    id: int
    galleries: List[Gallery] = []

    class Config:
        orm_mode = True


# Gallery with user
class GalleryWithUser(Gallery):
    user: User

    class Config:
        orm_mode = True


# Token for password restoration
class TokenResponse(BaseModel):
    token: str


# Search query
class Query(BaseModel):
    q: str
    user_id: int


# Request to download picture
class Download(BaseModel):
    id: int
    created_at: datetime
    requestor_id: int
    requestor: User
    owner_id: int
    gallery_id: int
    gallery: Gallery
    picture_id: int
    picture: Picture

    class Config:
        orm_mode = True


# Created token
class Token(BaseModel):
    access_token: str
    token_type: str


# Data inside token (user name)
class TokenData(BaseModel):
    username: Optional[str] = None


# Search suggestions
class Suggestion(BaseModel):
    suggestions: List[Tuple[str, int]]
