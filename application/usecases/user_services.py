from domain.entities.user import User
from infrastructure.db.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException
import bcrypt

class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def register(self, data:User):
        existing = await self.repo.get_by_email_or_username(data.email, data.username)
        if existing:
            raise HTTPException(status_code=400, detail="Email sudah digunakan")

        hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt())
        data.password = hashed_password.decode('utf-8')

        new_user = User(
            username=data.username,
            email=data.email,
            hashed_password=hashed_password
        )

        # Simpan ke DB
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user

    def login(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        token = create_access_token({"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}

    def get_current_user(self, email: str):
        return self.repo.get_by_email(email)
