# infrastructure/db/repositories/user_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from infrastructure.db.connection import database
from domain.entities.user import User
from infrastructure.db.models.user_model import UserModel  # Table SQLAlchemy

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_email_or_username(self, email: str, username: str):
        result = await self.session.execute(
            select(User).where(
                (User.email == email) | (User.username == username)
            )
        )
        return result.scalars().first()
    
    async def create_user(self, user: User):
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        user_id = await database.execute()
        return {**user.dict(), "id": user_id}

    # async def get_by_email(self, email: str):
    #     result = await self.session.execute(
    #         select(UserModel).where(UserModel.email == email)
    #     )
    #     user = result.scalars().first()  # only call once
    #     print(user)
    #     return user