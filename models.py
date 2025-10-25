from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    phone_number = Column(String(20))
    age = Column(Integer)
    gender = Column(String(10))
    religion = Column(String(50))
    city = Column(String(100))
    latitude = Column(String(50))
    longitude = Column(String(50))
    bio = Column(Text)
    language = Column(String(10), default='en')
    profile_photos = Column(Text)  # JSON string of photo file_ids
    registration_complete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Like(Base):
    __tablename__ = 'likes'
    
    id = Column(Integer, primary_key=True)
    liker_id = Column(Integer, nullable=False)
    liked_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)
    message_text = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Block(Base):
    __tablename__ = 'blocks'
    
    id = Column(Integer, primary_key=True)
    blocker_id = Column(Integer, nullable=False)
    blocked_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)