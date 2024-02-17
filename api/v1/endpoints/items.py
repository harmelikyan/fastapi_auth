from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from db.models import Session, get_db
from schemas import pydantic_schemas
from utils import items as item_crud


router = APIRouter()


@router.post("/{user_id}/items/", response_model=pydantic_schemas.Item)
async def create_item_for_user(user_id: int, item: pydantic_schemas.ItemCreate, db: Session = Depends(get_db)):
    return await item_crud.create_user_item(db=db, item=item, user_id=user_id)
