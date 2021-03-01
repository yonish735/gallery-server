from typing import List, Optional

from pydantic import BaseModel


class GalleryBase(BaseModel):
    title: str
    description: str
    private: bool
    image: Optional[str] = None


class GalleryCreate(GalleryBase):
    user_id: int


class Gallery(GalleryBase):
    id: int
    user_id: int

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


class User(UserBase):
    id: int
    galleries: List[Gallery] = []

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    token: str
