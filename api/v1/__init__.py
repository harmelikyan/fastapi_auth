from fastapi import APIRouter
from api.v1.endpoints import user
from api.v1 import auth

router = APIRouter()


router.include_router(router=user.router, prefix="/user", tags=["user"])
router.include_router(router=auth.router, prefix="/auth", tags=["auth"])


