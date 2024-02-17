from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.v1.auth import create_access_token, verify_password, oauth2_scheme
from schemas import pydantic_schemas
from schemas.pydantic_schemas import User

from sqlalchemy.orm import Session
from db import models
from utils import user as user_crud
from schemas import pydantic_schemas
from db.models import get_db
import os
from schemas.pydantic_schemas import Token

ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("JWT_TOKEN_EXPIRATION")

router = APIRouter()


@router.post("/register", response_model=pydantic_schemas.DBUser)
def create_user(user: pydantic_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)


@router.post("/login", response_model=Token)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, form_data.username)
    if not user:
        raise ("401", "Unothorized, user does not exist, or data is incorrect")
    if not verify_password(form_data.password, user.hashed_password):
        raise ("401", "password is incorrect")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/info", response_model=pydantic_schemas.DBUser)
async def read_user(user_id: int, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    db_user = await user_crud.check_user_token(token, db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# @router.get("/list_users", response_model=list[pydantic_schemas.DBUser])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = user_crud.get_users(db, skip=skip, limit=limit)
#     return users


# @router.get("/me", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return current_user
