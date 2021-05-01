from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.database.database import Base


# Description of database models

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    token = Column(String)

    # User has many Galleries
    galleries = relationship("Gallery", back_populates='user',
                             cascade="all, delete, delete-orphan")

    # The string representation of a User
    def __repr__(self):
        return "<User(id=%d,fullname='%s %s', email='%s')>" % (
            self.id, self.first_name, self.last_name,
            self.email)


# Gallery model
class Gallery(Base):
    __tablename__ = "galleries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    private = Column(Boolean)
    image = Column(String)
    filename = Column(String)

    # Gallery has many Pictures
    pictures = relationship("Picture", back_populates='gallery',
                            cascade="all, delete, delete-orphan")

    # Gallery belongs to User
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

    # The string representation of a Gallery
    def __repr__(self):
        return "<Gallery(userid='%s', id=%d, private='%s', title='%s')>" % (
            self.user.id, self.id, self.private, self.title)


# Picture model
class Picture(Base):
    __tablename__ = "pictures"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    private = Column(Boolean)
    image = Column(String)
    filename = Column(String)

    # Picture belongs to Gallery
    gallery_id = Column(Integer, ForeignKey("galleries.id"))
    gallery = relationship("Gallery")

    # The string representation of a Picture
    def __repr__(self):
        return "<Picture(gallery.id='%s', id=%d, title='%s')>" % (
            self.gallery.id, self.id, self.title)


# Download model
class Download(Base):
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    owner_id = Column(Integer, index=True)

    # Download belongs to User (requestor)
    requestor_id = Column(Integer, ForeignKey("users.id"))
    requestor = relationship("User")

    # Download belongs to Gallery
    gallery_id = Column(Integer, ForeignKey("galleries.id"))
    gallery = relationship("Gallery")

    # Download belongs to Picture
    picture_id = Column(Integer, ForeignKey("pictures.id"))
    picture = relationship("Picture")
