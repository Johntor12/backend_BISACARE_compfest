import os
from domain.entities.user import User
from infrastructure.db.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import bcrypt
from infrastructure.db.connection import get_db

from schemas.user_schema import UserCreate

oauth2_scheme = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "smart-assurance-with-ai")  # default if not set
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def register(self, data: UserCreate):
        # Check if user exists
        existing = await self.repo.get_by_email_or_username(str(data.email), data.username)
        if existing:
            raise HTTPException(status_code=400, detail="Email atau username sudah digunakan")

        # Hash password
        hashed_password = hash_password(data.password)

        # Create user
        new_user = User(
            username=data.username,
            email=str(data.email),
            password=hashed_password,
            nomor_telepon=data.nomor_telepon
        )

        # Save to DB without starting a new transaction
        saved_user = await self.repo.create_user(new_user)
        return saved_user

    async def login(self, identifier: str, password: str):
        user = await self.repo.get_by_identifier(identifier)  # async call
        if not user or not verify_password(password, user.password):  # sync call
            return HTTPException(status_code=401, detail="Email atau password salah")
        token = create_access_token({"sub": user.email})  # sync call
        return {"access_token": token, "token_type": "bearer"}

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials):
        if not credentials or not credentials.scheme:
            raise HTTPException(status_code=401, detail="Not authenticated")

        print("DEBUG CREDENTIALS:", credentials.scheme, credentials.credentials[:30])  # <--- tambahkan ini
        
        token = credentials.credentials
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(status_code=401, detail="Token tidak valid")
        except JWTError:
            raise HTTPException(status_code=401, detail="Token tidak dapat diverifikasi")
        
        user = await self.repo.get_by_identifier(identifier=email)
        if not user:
            raise HTTPException(status_code=401, detail="User tidak ditemukan")
        return user