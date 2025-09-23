from sqlalchemy.orm import Session
from domain.entities.user import User
from infrastructure.db.repositories.user_repo import UserRepository
from infrastructure.db.models.user_model import UserModel

class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    async def get_by_email(self, email: str):
        u = await self.db.query(UserModel).filter(UserModel.email == email).first()
        return  User(u.id, u.username, u.email, u.assword) if u else None

    async def get_by_id(self, id: int):
        u = await self.db.query(UserModel).filter(UserModel.id == id).first()
        return User(u.id, u.username, u.email, u.password) if u else None

    async def create(self, user: User):
        new_user = await UserModel(username=user.username, email=user.email, password=user.password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return User(new_user.id, new_user.username, new_user.email, new_user.password)
