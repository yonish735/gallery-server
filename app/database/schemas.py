from typing import List, Optional

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


class TokenResponse(BaseModel):
    token: str


class Query(BaseModel):
    q: str
    user_id: int


class Download(BaseModel):
    id: int
    requestor_id: int
    owner_id: int
    gallery_id: int
    picture_id: int
