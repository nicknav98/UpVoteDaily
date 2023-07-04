from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Session

from database import Base


class Submissions(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    url = Column(String, unique=True, index=True)
    votes = Column(Integer)
    
    submissionImage = Column(String, unique=True)
    
    owner_name = Column(String, ForeignKey('users.username'))
    owner = relationship("User", back_populates="submissions_by_owner", lazy=True)
    


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(120), unique=True, index=True)
    password = Column(String(128))
    is_active = Column(Boolean, default=True)
    avatar = Column(String, unique=True)
    submissions_by_owner = relationship("Submissions", back_populates='owner')
