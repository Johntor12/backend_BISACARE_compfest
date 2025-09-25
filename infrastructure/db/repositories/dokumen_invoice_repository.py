from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import List, Optional
from fastapi import HTTPException
from domain.entities.dokumen_invoice import DokumenInvoice
from infrastructure.db.models.dokumen_invoice_model import DokumenInvoiceModel
from schemas.dokumen_invoice_schema import DokumenInvoiceRequest, DokumenInvoiceResponse
from domain.entities.claim import Claim
from datetime import datetime

class DokumenInvoiceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_dokumen_invoice(self, dokumen_invoice: DokumenInvoice) -> DokumenInvoice:
        db_dokumen_invoice = DokumenInvoiceModel(
                                        dokumen_invoice_id=dokumen_invoice.dokumen_invoice_id,
                                        dokumen_invoice_url=dokumen_invoice.dokumen_invoice_url,
                                        user_id=dokumen_invoice.user_id
                                         )
        self.session.add(db_dokumen_invoice)
        await self.session.commit()
        await self.session.refresh(db_dokumen_invoice)
        return DokumenInvoiceResponse(
            id=db_dokumen_invoice.dokumen_invoice_id,
            dokumen_invoice_url=db_dokumen_invoice.dokumen_invoice_url,
            user_id=db_dokumen_invoice.user_id,
            created_at=datetime.now()
        )

    async def get_all_dokumen_invoice(self) -> List[DokumenInvoiceModel]:
        result = await self.session.execute(select(DokumenInvoiceModel).where(DokumenInvoiceModel.user))
        return result.scalars().all()
    
    async def get_all_dokumen_invoice_user(self, user_id: int) -> List[DokumenInvoiceModel]:
        dokumen_invoice = DokumenInvoiceModel()
        result = await self.session.execute(select(DokumenInvoiceModel).where(DokumenInvoiceModel.user_id==user_id))
        return result.scalars().all()
    
    async def get_dokumen_invoice_by_user_id(self, dokumen_invoice_id: int) -> Optional[DokumenInvoiceModel]:
        result = await self.session.execute(
            select(DokumenInvoiceModel).where(DokumenInvoiceModel.dokumen_invoice_id==dokumen_invoice_id)
        )
        dokumen_invoice = result.scalars().first()
        if dokumen_invoice:
            return result.scalars().first()
    
    async def get_dokumen_invoice_by_id(self, dokumen_invoice_id: int) -> Optional[DokumenInvoiceModel]:
        result = await self.session.execute(select(DokumenInvoiceModel).where((DokumenInvoiceModel.dokumen_invoice_id==dokumen_invoice_id)))
        dokumen_invoice = result.scalars().first()
        if dokumen_invoice:
            return dokumen_invoice

    async def update_dokumen_invoice(self, dokumen_invoice_id: int, dokumen_invoice: DokumenInvoiceModel, user_id: int) -> Optional[DokumenInvoiceModel]:
        dokumen_invoice = await self.get_dokumen_invoice_by_id(dokumen_invoice_id)
        if not dokumen_invoice:
            raise HTTPException(status_code=404, detail="dokumen_invoice tidak ditemukan")
        await self.session.execute(update(DokumenInvoiceModel).where(DokumenInvoiceModel.dokumen_invoice_id==dokumen_invoice_id and DokumenInvoiceModel.user_id==user_id))
        await self.session.commit()
        await self.session.refresh(dokumen_invoice)
        return dokumen_invoice

    async def delete_dokumen_invoice_by_id(self, dokumen_invoice_id: int):
        dokumen_invoice = await self.session.execute(select(DokumenInvoiceModel).where(DokumenInvoiceModel.id == dokumen_invoice_id))
        await self.session.delete(dokumen_invoice)
        await self.session.commit()
        return {"msg": "Aju banding berhasil dihapus!"}
    # async def delete_dokumen_invoice(self, dokumen_invoice_id: int) -> bool:
    #     dokumen_invoice = await self.get_dokumen_invoice_by_id(dokumen_invoice_id)
    #     if not dokumen_invoice:
    #         raise HTTPException(status_code=404, detail="dokumen_invoice tidak ditemukan")
    #     await self.session.delete(dokumen_invoice)
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