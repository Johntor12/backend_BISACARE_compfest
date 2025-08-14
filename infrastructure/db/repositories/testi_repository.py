from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import List, Optional

from infrastructure.db.models.testi_model import TestiModel
from domain.entities.testi import Testi

class TestiRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_testi(self, testi: Testi) -> TestiModel:
        db_testi = TestiModel(
            source_person=testi.source_person,
            image_person=testi.image_person,
            testi=testi.testi
        )
        self.session.add(db_testi)
        await self.session.commit()
        await self.session.refresh(db_testi)
        return db_testi

    async def get_all_testi(self) -> List[TestiModel]:
        result = await self.session.execute(select(TestiModel))
        return result.scalars().all()

    async def get_testi_by_id(self, testi_id: int) -> Optional[TestiModel]:
        result = await self.session.execute(
            select(TestiModel).where(TestiModel.testi_id == testi_id)
        )
        return result.scalars().first()

    async def update_testi(self, testi_id: int, testi: Testi) -> Optional[TestiModel]:
        await self.session.execute(
            update(TestiModel)
            .where(TestiModel.testi_id == testi_id)
            .values(
                source_person=testi.source_person,
                image_person=testi.image_person,
                testi=testi.testi
            )
        )
        await self.session.commit()
        return await self.get_testi_by_id(testi_id)

    async def delete_testi(self, testi_id: int) -> bool:
        await self.session.execute(delete(TestiModel).where(TestiModel.testi_id == testi_id))
        await self.session.commit()
        return True
