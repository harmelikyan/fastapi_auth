from pydantic import EmailStr
from sqlalchemy.orm import Session
from api.v1.auth import create_hash_password

from db import models

from schemas import pydantic_schemas
from fastapi import Depends, HTTPException, status

from db.models import get_db
import os
from jose import JWTError, jwt


ALGORITHM = os.environ.get("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("JWT_TOKEN_EXPIRATION")
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: EmailStr):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


async def check_user_token(token: str, db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = pydantic_schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# TODO: check if the user is allowed to get access to info
def verify_user(user):
    check_user_token()


def create_user(user: pydantic_schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = create_hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
