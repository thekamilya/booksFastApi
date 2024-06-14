from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Book(Base):
    __tablename__ = "Books"
    num_of_people_rated = 0
    overall = 0
    rating = 0
    id = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)
    image_resource = Column(String)
    comments = relationship("Comment", back_populates="book")




class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    comments = relationship("Comment", back_populates="user")


class Comment(Base):
    __tablename__ = "Comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    book_id = Column(String, ForeignKey('Books.id'))
    book = relationship("Book", back_populates="comments")
    user_id = Column(Integer, ForeignKey('Users.id'))
    user = relationship("User", back_populates="comments")

