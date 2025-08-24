from domain.entities.user import User
from infrastructure.db.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException
import bcrypt

from schemas.user_schema import UserCreate


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
        self.repo.session.add(new_user)
        await self.repo.session.flush()  # ensures ID is generated
        await self.repo.session.commit()
        await self.repo.session.refresh(new_user)
        return new_user

    async def login(self, email: str, password: str):
        user = await self.repo.get_by_email_or_username(email, None)  # kirim None untuk username
        if not user or not verify_password(password, user.password):
            return None
        token = create_access_token({"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}

    async def get_current_user(self, email: str):
        return await self.repo.get_by_email_or_username(email, None)  # tambahkan None untuk username
