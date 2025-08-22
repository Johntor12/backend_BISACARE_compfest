from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import List, Optional
from fastapi import HTTPException

from infrastructure.db.models.claim_model import ClaimModel
from infrastructure.db.models.claim_event_model import ClaimEventModel
from infrastructure.db.models.claim_document_model import ClaimDocumentModel
from domain.entities.claim import Claim

class ClaimRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_claim(self, claim: Claim) -> ClaimModel:
        db_claim = ClaimModel(**claim.__dict__)
        self.session.add(db_claim)
        await self.session.commit()
        await self.session.flush()
        await self.session.refresh(db_claim)
        return Claim(**db_claim.__dict__)

    async def get_all_claims(self) -> List[ClaimModel]:
        result = await self.session.execute(select(ClaimModel))
        return result.scalars().all()

    # async def get_claim_by_id(self, claim_id: int) -> Optional[ClaimModel]:
    #     result = await self.session.execute(
    #         select(ClaimModel).where(ClaimModel.id == claim_id)
    #     )
    #     return result.scalars().first()
    
    async def get_claim_by_id(self, claim_id: int) -> Claim | None:
        result = await self.session.execute(select(ClaimModel).where(ClaimModel.id == claim_id))
        claim = result.scalars().first()
        return Claim(**claim.__dict__) if claim else None
    
    async def get_claims_by_user_id(self, user_id: int) -> Claim:
        result = await self.session.execute(select(ClaimModel)
                                                .where(ClaimModel.user_id == user_id))
        claim = result.scalars().all()

    async def update_claim(self, claim_id: int, claim: Claim) -> Optional[ClaimModel]:
        claim = await self.get_claim_by_id(claim_id)
        if not claim:
            None
        claim.user_id = claim.user_id
        claim.status = claim.status
        await self.session.commit()
        await self.session.refresh(claim)
        return claim
    
    async def update_claim_status(self, claim_id: int, status: str):
        claim = await self.get_claim_by_id(claim_id)
        if not claim:
            None
        claim.status = status
        await self.session.commit()
        await self.session.refresh(claim)
        return claim

    async def delete_claim(self, claim_id: int) -> bool:
        claim = await self.get_claim_by_id(claim_id)
        if not claim:
            return False
        await self.session.delete(claim)
        await self.session.commit()
        return True
    

    # Claim Events (Tracker)
    async def add_claim_event(self, claim_id: int, step: str, status: str, note: Optional[str] = None) -> ClaimEventModel:
        event = ClaimEventModel(claim_id=claim_id, step=step, status=status, note=note)
        self.session.add(event)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(event)
        return event
    
    async def get_claim_event_by_claim_id(self, claim_id: int) -> List[ClaimEventModel]:
        result = await self.session.execute(
            select(ClaimEventModel)
            .where(ClaimEventModel.claim_id == claim_id)
            .order_by(ClaimEventModel.timestamp.asc())
        )
        return result.scalars().all()
    
    async def delete_claim_event_by_claim_id(self, claim_id: int) -> int:
        result = await self.session.execute(
            delete(ClaimEventModel).where(ClaimEventModel.claim_id == claim_id).returning(ClaimEventModel.id)
        )
        await self.session.commit()
        deleted_rows = len(result.fetchall())
        return deleted_rows


    # Claim Documents (Slip Digital)
    async def add_claim_document(self, claim_id: int, file_url: str, file_type: str) -> ClaimDocumentModel:
        doc = ClaimDocumentModel(claim_id=claim_id, file_url=file_url, file_type=file_type)
        self.session.add(doc)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(doc)
        return doc
    
    async def get_claim_document_by_claim_id(self, claim_id: int) -> Optional[ClaimDocumentModel]:
        """
        Ambil dokumen terbaru untuk 'slip digital'
        """
        result = await self.session.execute(
            select(ClaimDocumentModel)
            .where(ClaimDocumentModel.claim_id == claim_id)
            .order_by(ClaimDocumentModel.uploaded_at.desc())
            .limit(1)
        )
        return result.scalars().first()

    async def get_all_documents_by_claim_id(self, claim_id: int) -> List[ClaimDocumentModel]:
        result = await self.session.execute(
            select(ClaimDocumentModel)
            .where(ClaimDocumentModel.claim_id == claim_id)
            .order_by(ClaimDocumentModel.uploaded_at.desc())
        )
        return result.scalars().all()