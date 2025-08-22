from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from domain.entities.testi import Testi
from application.usecases.testi_services import TestiService
from infrastructure.db.repositories.testi_repository import TestiRepository
from infrastructure.db.connection import get_db

router = APIRouter(prefix="/testi", tags=["Testi"])

@router.post("/", response_model=Testi)
async def create_testi(testi: Testi, db: AsyncSession = Depends(get_db)):
    repo = TestiRepository(db)
    service = TestiService(repo)
    return await service.create_testi(testi)

@router.get("/", response_model=List[Testi])
async def list_testi(db: AsyncSession = Depends(get_db)):
    repo = TestiRepository(db)
    service = TestiService(repo)
    return await service.get_all_testi()

@router.get("/{testi_id}", response_model=Testi)
async def get_testi(testi_id: int, db: AsyncSession = Depends(get_db)):
    repo = TestiRepository(db)
    service = TestiService(repo)
    testi = await service.get_testi_by_id(testi_id)
    if not testi:
        raise HTTPException(status_code=404, detail="Testi not found")
    return testi

@router.put("/{testi_id}", response_model=Testi)
async def update_testi(testi_id: int, testi: Testi, db: AsyncSession = Depends(get_db)):
    repo = TestiRepository(db)
    service = TestiService(repo)
    updated = await service.update_testi(testi_id, testi)
    if not updated:
        raise HTTPException(status_code=404, detail="Testi not found")
    return updated

@router.delete("/{testi_id}")
async def delete_testi(testi_id: int, db: AsyncSession = Depends(get_db)):
    repo = TestiRepository(db)
    service = TestiService(repo)
    success = await service.delete_testi(testi_id)
    if not success:
        raise HTTPException(status_code=404, detail="Testi not found")
    return {"message": "Testi deleted successfully"}
