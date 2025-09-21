from infrastructure.db.repositories.slip_repository import SlipRepository
from infrastructure.db.models.slip_model import SlipModel
from schemas.slip_schema import SlipCreate, SlipUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

class SlipService:
    def __init__(self, session: AsyncSession):
        self.repo = SlipRepository(session)

    async def create_slip(self, data: SlipCreate, user_id: int):
        slip = SlipModel(user_id=user_id, **data.dict())
        return await self.repo.create(slip)

    async def get_slip(self, slip_id: int, user_id: int):
        slip = await self.repo.get_by_id(slip_id)
        if not slip or slip.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slip tidak ditemukan")
        return slip

    async def get_user_slips(self, user_id: int):
        return await self.repo.get_all_by_user(user_id)

    async def update_slip(self, slip_id: int, data: SlipUpdate, user_id: int):
        slip = await self.get_slip(slip_id, user_id)
        return await self.repo.update(slip, data.dict(exclude_unset=True))

    async def delete_slip(self, slip_id: int, user_id: int):
        slip = await self.get_slip(slip_id, user_id)
        await self.repo.delete(slip)
        return {"msg": "Slip berhasil dihapus"}
