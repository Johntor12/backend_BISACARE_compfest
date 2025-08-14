from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from domain.entities.claim import Claim
from application.usecases.claim_services import ClaimService
from infrastructure.db.repositories.claim_repository import ClaimRepository
from infrastructure.db.connection import get_db

router = APIRouter(prefix="/claims", tags=["Claims"])

@router.post("/", response_model=Claim)
async def create_claim(claim: Claim, db: AsyncSession = Depends(get_db)):
    repo = ClaimRepository(db)
    service = ClaimService(repo)
    return await service.create_claim(claim)

@router.get("/", response_model=List[Claim])
async def list_claims(db: AsyncSession = Depends(get_db)):
    repo = ClaimRepository(db)
    service = ClaimService(repo)
    return await service.get_all_claims()

@router.get("/{claim_id}", response_model=Claim)
async def get_claim(claim_id: int, db: AsyncSession = Depends(get_db)):
    repo = ClaimRepository(db)
    service = ClaimService(repo)
    claim = await service.get_claim_by_id(claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim

@router.put("/{claim_id}", response_model=Claim)
async def update_claim(claim_id: int, claim: Claim, db: AsyncSession = Depends(get_db)):
    repo = ClaimRepository(db)
    service = ClaimService(repo)
    updated = await service.update_claim(claim_id, claim)
    if not updated:
        raise HTTPException(status_code=404, detail="Claim not found")
    return updated

@router.delete("/{claim_id}")
async def delete_claim(claim_id: int, db: AsyncSession = Depends(get_db)):
    repo = ClaimRepository(db)
    service = ClaimService(repo)
    success = await service.delete_claim(claim_id)
    if not success:
        raise HTTPException(status_code=404, detail="Claim not found")
    return {"message": "Claim deleted successfully"}
