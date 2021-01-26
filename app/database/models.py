from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)

    galleries = relationship("Gallery")


class Gallery(Base):
    __tablename__ = "galleries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    private = Column(Boolean)
    image = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")
