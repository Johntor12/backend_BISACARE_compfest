from typing import List
from domain.entities.testi import Testi
from infrastructure.db.repositories.testi_repository import TestiRepository

class TestiService:
    def __init__(self, testi_repository: TestiRepository):
        self.testi_repository = testi_repository

    async def create_testi(self, testi: Testi):
        return await self.testi_repository.create_testi(testi)

    async def get_all_testi(self):
        return await self.testi_repository.get_all_testi()

    async def get_testi_by_id(self, testi_id: int):
        return await self.testi_repository.get_testi_by_id(testi_id)

    async def update_testi(self, testi_id: int, testi: Testi):
        return await self.testi_repository.update_testi(testi_id, testi)

    async def delete_testi(self, testi_id: int):
        return await self.testi_repository.delete_testi(testi_id)
