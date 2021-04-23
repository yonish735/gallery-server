from typing import List, Optional, Tuple
from datetime import datetime
from pydantic import BaseModel


class GalleryBase(BaseModel):
    title: str
    description: str
    private: bool
    image: Optional[str] = None
    filename: Optional[str] = None


class GalleryCreate(GalleryBase):
    user_id: int


class Gallery(GalleryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class PictureBase(BaseModel):
    title: str
    description: str
    private: bool
    image: Optional[str] = None
    filename: Optional[str] = None


class PictureCreate(PictureBase):
    gallery_id: int


class Picture(PictureBase):
    id: int
    gallery_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    password: str


class UserForgotPassword(BaseModel):
    email: str
    password: str
    token: str


class User(UserBase):
    id: int
    galleries: List[Gallery] = []

    class Config:
        orm_mode = True


class GalleryWithUser(Gallery):
    user: User

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    token: str


class Query(BaseModel):
    q: str
    user_id: int


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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Suggestion(BaseModel):
    suggestions: List[Tuple[str, int]]
