from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from schemas import pydantic_schemas
from schemas.pydantic_schemas import User

# from api.v1.auth import get_current_active_user
from sqlalchemy.orm import Session
from db import models
from utils import user as user_crud
from utils import items as item_crud
from schemas import pydantic_schemas
from db.models import get_db


router = APIRouter()


@router.post("/", response_model=pydantic_schemas.DBUser)
def create_user(user: pydantic_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)


@router.get("/", response_model=list[pydantic_schemas.DBUser])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=pydantic_schemas.DBUser)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/items/", response_model=pydantic_schemas.Item)
def create_item_for_user(user_id: int, item: pydantic_schemas.ItemCreate, db: Session = Depends(get_db)):
    return item_crud.create_user_item(db=db, item=item, user_id=user_id)


# @router.get("/me", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return current_user
