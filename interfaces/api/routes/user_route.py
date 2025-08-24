from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import decode_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.connection import get_db
from application.usecases.user_services import UserService
from infrastructure.db.repositories.user_repo_impl import UserRepositoryImpl

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter()

@router.get("/me")
async def get_me(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload.get("sub")
    service = UserService(db)
    user = await service.get_current_user(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"email": user.email, "username": user.username}
