from datetime import time, timedelta
from typing import Union
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

import crud
import models
import schemas
import password
import authentication
import uvicorn


from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List

models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token",
    scheme_name="JWT"
)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/get_current_user', response_model=schemas.User)
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, password.SECRET_KEY, algorithms=[password.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post('/register', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: SessionLocal = Depends(get_db)):
    hashed_password = password.get_password_hash(user.password)
    db_user = crud.get_user_by_email(db, email=user.email)
    db_username = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    if db_username:
        raise HTTPException(status_code=400, detail="User with this username already exists")
    return crud.create_user(db=db, user=user, password_hashed=hashed_password)

@app.get('/users/', response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post('/users/{username}/submissions/', response_model=schemas.Submission)
def create_user_building(username: str, submission: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_submission(db=db, username=username, submission=submission)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, username=form_data.username, user_password=form_data.password)
    if not user:
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=password.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.User)
async def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, password.SECRET_KEY, algorithms=[password.ALGORITHM])
        token_data = schemas.TokenData(username=payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid", headers={"WWW-Authenticate": "Bearer"})
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found", headers={"WWW-Authenticate": "Bearer"})
    return user


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")