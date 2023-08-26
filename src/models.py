import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    phone = Column(String(30), nullable=False)

    def serialize(self):
        return {
            "username": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email, 
            "phone": self.phone,
        }

class Follower(Base):
    __tablename__ = 'follower'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    user_from_id = Column(Integer, nullable=False)
    user_to_id = Column(Integer, nullable=False)      
    # person_id = Column(Integer, ForeignKey('person.id'))
    # person = relationship(Person)

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, ForeignKey=True)
    user_id = Column(Integer, nullable=False)

    def serialize(self):
        return {
            "user_id": self.user_id,
        }

class SavedPosts(Base):
    __tablename__ = 'saved_posts'
    user_from_id = Column(Integer, nullable=False)
    user_to_id = Column(Integer, nullable=False) 

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
