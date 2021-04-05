from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    hashed_password = Column(String)

    galleries = relationship("Gallery", back_populates='user',
                             cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<User(id=%d,fullname='%s %s', email='%s')>" % (
            self.id, self.first_name, self.last_name,
            self.email)


class Gallery(Base):
    __tablename__ = "galleries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    private = Column(Boolean)
    image = Column(String)
    filename = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")

    def __repr__(self):
        return "<Gallery(userid='%s', id=%d, private='%s', title='%s')>" % (
            self.user.id, self.id, self.private, self.title)


class Picture(Base):
    __tablename__ = "pictures"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    private = Column(Boolean)
    image = Column(String)
    filename = Column(String)
    gallery_id = Column(Integer, ForeignKey("galleries.id"))

    gallery = relationship("Gallery")

    def __repr__(self):
        return "<Picture(gallery.id='%s', id=%d, title='%s')>" % (
            self.gallery.id, self.id, self.title)


class Downloads(Base):
    __tablename__ = "downloads"
    id = Column(Integer, primary_key=True, index=True)
    requestor_id = Column(Integer)
    owner_id = Column(Integer, index=True)
    gallery_id = Column(Integer)
    picture_id = Column(Integer)
