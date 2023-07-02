from typing import List, Union
from pydantic import BaseModel, HttpUrl, AnyUrl
import pandas as pd

class SubmissionBase(BaseModel):
    id: int
    title: str
    url: HttpUrl
    votes: int
    class Config:
        orm_mode = True

class Submission(SubmissionBase):
    class Config:
        orm_mode = True

class SubmissionCreate(SubmissionBase):
    pass

class UserBase(BaseModel):
    username: str

class User(UserBase):
    id: int
    submissions_by_owner: List[SubmissionBase] 

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str

class UserDB(User):
    hashed_password: str 
    class Config:
        orm_mode=True


class Token(BaseModel):
    token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: Union[str, None]

    class Config:
        orm_mode = True


