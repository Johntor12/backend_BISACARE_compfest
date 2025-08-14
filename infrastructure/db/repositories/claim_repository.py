from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import List, Optional

from infrastructure.db.models.claim_model import ClaimModel
from domain.entities.claim import Claim

class ClaimRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_claim(self, claim: Claim) -> ClaimModel:
        db_claim = ClaimModel(**claim.dict())
        self.session.add(db_claim)
        await self.session.commit()
        await self.session.refresh(db_claim)
        return db_claim

    async def get_all_claims(self) -> List[ClaimModel]:
        result = await self.session.execute(select(ClaimModel))
        return result.scalars().all()

    async def get_claim_by_id(self, claim_id: int) -> Optional[ClaimModel]:
        result = await self.session.execute(
            select(ClaimModel).where(ClaimModel.id == claim_id)
        )
        return result.scalars().first()

    async def update_claim(self, claim_id: int, claim: Claim) -> Optional[ClaimModel]:
        await self.session.execute(
            update(ClaimModel).where(ClaimModel.id == claim_id).values(**claim.dict())
        )
        await self.session.commit()
        return await self.get_claim_by_id(claim_id)

    async def delete_claim(self, claim_id: int) -> bool:
        await self.session.execute(delete(ClaimModel).where(ClaimModel.id == claim_id))
        await self.session.commit()
        return True

    async def update_claim_status(self, claim_id: int, status: str):
        claim = await self.claim_repository.get_claim_by_id(claim_id)
        if not claim:
            return None
        claim.status = status
        await self.claim_repository.session.commit()
        await self.claim_repository.session.refresh(claim)
        return claim