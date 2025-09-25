from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import List, Optional
from fastapi import HTTPException
from domain.entities.aju_banding import AjuBanding
from infrastructure.db.models.aju_banding_model import AjuBandingModel
from schemas.aju_banding_schema import AjuBandingRequest, AjuBandingResponse
from domain.entities.claim import Claim
from datetime import datetime

class AjuBandingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_aju_banding(self, aju_banding: AjuBanding) -> AjuBanding:
        db_aju_banding = AjuBandingModel(
                                        aju_banding_id=aju_banding.aju_banding_id,
                                        aju_banding_url=aju_banding.aju_banding_url,
                                        user_id=aju_banding.user_id
                                         )
        self.session.add(db_aju_banding)
        await self.session.commit()
        await self.session.refresh(db_aju_banding)
        return AjuBandingResponse(
            id=db_aju_banding.aju_banding_id,
            aju_banding_url=db_aju_banding.aju_banding_url,
            user_id=db_aju_banding.user_id,
            created_at=datetime.now()
        )

    async def get_all_aju_banding(self) -> List[AjuBandingModel]:
        result = await self.session.execute(select(AjuBandingModel).where(AjuBandingModel.user))
        return result.scalars().all()
    
    async def get_all_aju_banding_user(self, user_id: int) -> List[AjuBandingModel]:
        aju_banding = AjuBandingModel()
        result = await self.session.execute(select(AjuBandingModel).where(AjuBandingModel.user_id==user_id))
        return result.scalars().all()
    
    async def get_aju_banding_by_id(self, aju_banding_id: int) -> AjuBandingModel:
        result = await self.session.execute(select(AjuBandingModel).where(AjuBandingModel.aju_banding_id==aju_banding_id))
        aju_banding = result.scalars().first()
        if aju_banding:
            return aju_banding

    async def update_aju_banding(self, aju_banding_id: int, aju_banding: AjuBandingModel, user_id: int) -> Optional[AjuBandingModel]:
        aju_banding = await self.get_aju_banding_by_id(aju_banding_id)
        if not aju_banding:
            raise HTTPException(status_code=404, detail="aju_banding tidak ditemukan")
        await self.session.execute(update(AjuBandingModel).where(AjuBandingModel.aju_banding_id==aju_banding_id and AjuBandingModel.user_id==user_id))
        await self.session.commit()
        await self.session.refresh(aju_banding)
        return aju_banding

    async def delete_aju_banding_by_id(self, aju_banding_id: int):
        aju_banding = await self.session.execute(select(AjuBandingModel).where(AjuBandingModel.aju_banding_id == aju_banding_id))
        await self.session.delete(aju_banding)
        await self.session.commit()
        return {"msg": "Aju banding berhasil dihapus!"}
    # async def delete_aju_banding(self, aju_banding_id: int) -> bool:
    #     aju_banding = await self.get_aju_banding_by_id(aju_banding_id)
    #     if not aju_banding:
    #         raise HTTPException(status_code=404, detail="aju_banding tidak ditemukan")
    #     await self.session.delete(aju_banding)
    #     await self.session.commit()
    #     return True
    

    # # Claim Events (Tracker)
    # async def add_claim_event(self, claim_id: int, step: str, status: str, note: Optional[str] = None) -> ClaimEventModel:
    #     event = ClaimEventModel(claim_id=claim_id, step=step, status=status, note=note)
    #     self.session.add(event)
    #     await self.session.flush()
    #     await self.session.commit()
    #     await self.session.refresh(event)
    #     return event
    
    # async def get_claim_event_by_claim_id(self, claim_id: int) -> List[ClaimEventModel]:
    #     result = await self.session.execute(
    #         select(ClaimEventModel)
    #         .where(ClaimEventModel.claim_id == claim_id)
    #         .order_by(ClaimEventModel.timestamp.asc())
    #     )
    #     return result.scalars().all()
    
    # async def delete_claim_event_by_claim_id(self, claim_id: int) -> int:
    #     result = await self.session.execute(
    #         delete(ClaimEventModel).where(ClaimEventModel.claim_id == claim_id).returning(ClaimEventModel.id)
    #     )
    #     await self.session.commit()
    #     deleted_rows = len(result.fetchall())
    #     return deleted_rows


    # # Claim Documents (Slip Digital)
    # async def add_claim_document(self, claim_id: int, file_url: str, file_type: str) -> ClaimDocumentModel:
    #     doc = ClaimDocumentModel(claim_id=claim_id, file_url=file_url, file_type=file_type)
    #     self.session.add(doc)
    #     await self.session.flush()
    #     await self.session.commit()
    #     await self.session.refresh(doc)
    #     return doc
    
    # async def get_claim_document_by_claim_id(self, claim_id: int) -> Optional[ClaimDocumentModel]:
    #     """
    #     Ambil dokumen terbaru untuk 'slip digital'
    #     """
    #     result = await self.session.execute(
    #         select(ClaimDocumentModel)
    #         .where(ClaimDocumentModel.claim_id == claim_id)
    #         .order_by(ClaimDocumentModel.uploaded_at.desc())
    #         .limit(1)
    #     )
    #     return result.scalars().first()

    # async def get_all_documents_by_claim_id(self, claim_id: int) -> List[ClaimDocumentModel]:
    #     result = await self.session.execute(
    #         select(ClaimDocumentModel)
    #         .where(ClaimDocumentModel.claim_id == claim_id)
    #         .order_by(ClaimDocumentModel.uploaded_at.desc())
    #     )
    #     return result.scalars().all()