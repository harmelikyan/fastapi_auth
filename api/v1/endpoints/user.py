from typing import Annotated
from fastapi import APIRouter, Depends
from api.v1.schemas.pydantic_schemas import User
from api.v1.auth import get_current_active_user


router = APIRouter()




@router.get("/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


