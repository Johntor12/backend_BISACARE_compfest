from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from infrastructure.db.models.slip_model import SlipModel

class SlipRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, slip: SlipModel):
        self.session.add(slip)
        await self.session.commit()
        await self.session.refresh(slip)
        return slip

    async def get_by_id(self, slip_id: int):
        result = await self.session.execute(select(SlipModel).filter(SlipModel.slip_id == slip_id))
        return result.scalars().first()

    async def get_all_by_user(self, user_id: int):
        result = await self.session.execute(select(SlipModel).filter(SlipModel.user_id == user_id))
        return result.scalars().all()

    async def update(self, slip: SlipModel, data: dict):
        for key, value in data.items():
            setattr(slip, key, value)
        await self.session.commit()
        await self.session.refresh(slip)
        return slip

    async def delete(self, slip: SlipModel):
        await self.session.delete(slip)
        await self.session.commit()
