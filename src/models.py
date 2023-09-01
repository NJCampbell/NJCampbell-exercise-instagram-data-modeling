import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    user_name = Column (String(250), unique = True, nullable = False)
    password = Column(String(250), nullable=False)
    email =  Column (String(250), unique = True, nullable = False)
    full_name =  Column (String(250), nullable = False)
    bio  = Column (String(300),nullable = True)
    profile_picture = Column(String)
    post = relationship ('Post', back_populates = 'user')
    follower = relationship ('Follower' , back_populates = 'follower' , lazy ='dynamic')
    following = relationship ('Following', back_populates = 'following' , lazy = 'dynamic')

    def serialize (self):
        return{
            'user_name' : self.user_name,
            'email' : self.email,
            'full_name' : self. full_name,
            'bio' : self.bio,
            'profile_picture' : self.profile_picture
        }
   
class Post(Base):
    __tablename__ = 'posts'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    user_id = Column (Integer, ForeignKey('users.id'))
    image_url = Column (String(150), nullable = False)
    caption = Column (String(300), nullable = True)
    location = Column (String(300), nullable = True)
    post_time = Column(DateTime, default = datetime.datetime.utcnow)
    user = relationship('User' ,back_populates = 'post')
    comment = relationship ('Comment', back_populates = 'user')


    def to_dict(self):
        return {
            'user_id' : self.user_id,
            'image_url' : self.image_url,
            'caption': self. caption,
            'location' : self.location,
            'post_time': self.post_time
        }
    

class Comment (Base):
    __tablename__ = 'comments'
    id = Column (Integer , primary_key = True)
    user_id = Column (Integer, ForeignKey('users.id'))
    post_id = Column (Integer, ForeignKey('posts.id'))
    text_comment = Column (String (250), nullable = False)
    comment_time = Column (DateTime , default = datetime.datetime.utcnow)
    user = relationship ('User')
    post = relationship ('Post', back_populates = 'comment')
    like = relationship ('Like', back_populates ='user')

    def serialize (self):
        return{
            'user_id': self.user_id,
            'post_id': self.post_id,
            'text_comment': self.text_comment,
            'comment_time': self.comment_time
        }



class Like (Base):
    __tablename__ = 'likes'
    id = Column (Integer, primary_key = True)
    user_id = Column (Integer , ForeignKey ('users.id'))
    post_id = Column (Integer, ForeignKey('posts.id'))
    count_likes = Column (Integer)
    like_time = Column (DateTime, default = datetime.datetime.utcnow)
    post = relationship ('Post' , back_populates = 'like')
    user = relationship ('User')
    

    def serialize (self):
        return{
            'user_id': self.user_id,
            'post_id' : self.post_id,
            'count_likes': self.count_likes,
            'like_time' : self.like_time
        }

class Follower (Base) :
    __tablename__ = 'followers'
    id = Column (Integer , primary_key = True)
    user_id = Column (Integer , ForeignKey ('users.id'))
    follower_time = Column (DateTime , default = datetime.datetime.utcnow)
    count_followers = Column (Integer)
    user = relationship ('User' , back_populates = 'follower')

    def serialize (self):
        return{
            'user_id': self.user_id,
            'followe_time' : self.follower_time,
            'count_followers' : self.count_followers
        }

class Following (Base):
    __tablename__ ='followings'
    id = Column (Integer, primary_key = True)
    user_id = Column (Integer, ForeignKey ('users.id'))
    count_following = Column (Integer)
    following_time = Column (DateTime, default = datetime.datetime.utcnow)
    user = relationship ('User' , back_populates = 'following')

    def serialize (self):
        return{
            'user_id' : self.user_id,
            'count_following' : self.count_following,
            'following_time' : self. following_time
        }

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e