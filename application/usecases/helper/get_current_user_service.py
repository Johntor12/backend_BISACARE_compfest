from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from application.usecases.user_services import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.connection import get_db

oauth2_scheme = HTTPBearer()

async def get_current_user_service(
    db: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
):
    service = UserService(db)
    return await service.get_current_user(credentials)
