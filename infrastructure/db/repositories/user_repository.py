# infrastructure/db/repositories/user_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from infrastructure.db.connection import database
from domain.entities.user import User
from infrastructure.db.models.user_model import UserModel  # Table SQLAlchemy

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_email_or_username(self,  email: str, identifier: str) -> User | None :
        query = select(UserModel).where(
            (UserModel.email == identifier) | (UserModel.username == identifier)
        )
        result = await self.session.execute(query)
        if not result:
            return None
            
        model = result.scalars().first()
        if model:
            return User(
                id=model.id,
                username=model.username,
                email=model.email,
                password=model.password,
                nomor_telepon=model.nomor_telepon
            )
        return None

    async def get_by_identifier(self, identifier: str):
        result = await self.session.execute(
            select(UserModel).where(
                (UserModel.email == identifier) | (UserModel.username == identifier)
            )
        )
        model = result.scalars().first()
        if model:
            return User(
                id=model.id,
                username=model.username,
                email=model.email,
                password=model.password,
                nomor_telepon=model.nomor_telepon
            )
        return None

    async def create_user(self, user: User) -> User:
        model = UserModel(
            username=user.username,
            email=user.email,
            password=user.password,
            nomor_telepon=user.nomor_telepon
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        # 3. Mapping kembali ke Entity
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            password=model.password,
            nomor_telepon=model.nomor_telepon
        )

    # async def get_by_email(self, email: str):
    #     result = await self.session.execute(
    #         select(UserModel).where(UserModel.email == email)
    #     )
    #     user = result.scalars().first()  # only call once
    #     print(user)
    #     return user