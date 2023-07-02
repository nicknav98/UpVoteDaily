from datetime import timedelta, datetime
from typing import Union

from jose import jwt
from sqlalchemy.orm import Session

import models
import schemas
import password


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()



def get_submission(db: Session, id: int):
    return db.query(models.Submissions).filter(models.Submissions.id == id).first()

def get_all_submissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Submissions).offset(skip).limit(limit).all()


def get_user_submission(db:Session, owner: str):
    return db.query(models.Submissions).filter(models.Submissions.owner == owner).all()

def create_user_submission(db:Session, user: schemas.User, submissiom: schemas.SubmissionCreate):
    db_submission = models.Submissions(title = submissiom.title, url = submissiom.url, votes = submissiom.votes, submissionImage=submissiom.submissionImage, owner=user.username, avatar=user.avatar)
    db.add(db_submission)
    db.commit
    db.refresh(db_submission)
    return db_submission




def create_user(db: Session, user: schemas.UserCreate, password_hashed: schemas.UserDB):
    db_user = models.User(username=user.username, password=password_hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, password.SECRET_KEY, algorithm=password.ALGORITHM)
    return encoded_jwt


def create_refresh_token(username: str):
    return create_access_token({'username': username}, expires_delta=timedelta(days=7))


def authenticate_user(db: Session, username: str, user_password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not password.verify_password(user_password, user.password):
        return False
    return user