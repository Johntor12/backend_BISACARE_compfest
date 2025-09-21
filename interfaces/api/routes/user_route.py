from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.connection import get_db
from application.usecases.user_services import UserService, get_current_user_service
from schemas.user_schema import UserData

router = APIRouter()

@router.get("/me", response_model=UserData)
async def get_me(current_user = Depends(get_current_user_service)):
    return current_user
