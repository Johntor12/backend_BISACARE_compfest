from fastapi import HTTPException
from typing import List
from domain.entities.testi import Testi
from application.usecases.testi_services import TestiUseCase

class TestiController:
    def __init__(self, testi_usecase: TestiUseCase):
        self.testi_usecase = testi_usecase

    async def create_testi(self, testi: Testi) -> dict:
        testi_id = await self.testi_usecase.create_testi(testi)
        return {"testi_id": testi_id}

    async def list_testi(self) -> List[Testi]:
        return await self.testi_usecase.list_testi()

    async def get_testi(self, testi_id: int) -> Testi:
        testi = await self.testi_usecase.get_testi(testi_id)
        if not testi:
            raise HTTPException(status_code=404, detail="Testi not found")
        return testi

    async def update_testi(self, testi_id: int, testi: Testi) -> dict:
        success = await self.testi_usecase.update_testi(testi_id, testi)
        if not success:
            raise HTTPException(status_code=404, detail="Testi not found")
        return {"message": "Testi updated successfully"}

    async def delete_testi(self, testi_id: int) -> dict:
        success = await self.testi_usecase.delete_testi(testi_id)
        if not success:
            raise HTTPException(status_code=404, detail="Testi not found")
        return {"message": "Testi deleted successfully"}
