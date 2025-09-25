from infrastructure.db.repositories.dokumen_invoice_repository import DokumenInvoiceRepository
from infrastructure.storage.supabase_storage import SupabaseStorage
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.dokumen_invoice import DokumenInvoice
from schemas.dokumen_invoice_schema import DokumenInvoiceRequest, DokumenInvoiceResponse
from infrastructure.db.models.dokumen_invoice_model import DokumenInvoiceModel
from application.usecases.helper.get_current_user_service import get_current_user_service
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, UploadFile, Depends
from typing import Optional
import datetime
import logging
import os, shutil, uuid


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads/insurance"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class DokumenInvoiceService:
    def __init__(self, session: AsyncSession, storage: SupabaseStorage):
        self.repo = DokumenInvoiceRepository(session)
        self.storage = storage


    async def save_file(self, file: UploadFile, prefix:str) -> str:
        ext = os.path.split(file.filename)[1]
        filename = f"{prefix}_{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return filename

    async def create_dokumen_invoice(self, dokumen_invoice: Optional[UploadFile], current_user_id: int ) -> DokumenInvoice:
        
        # Upload file ke Supabase
        dokumen_invoice_url = await self.storage.upload_file(dokumen_invoice, "dokumen_invoice") if dokumen_invoice else None
        
        dokumen_invoice_form = DokumenInvoice(
            dokumen_invoice_url=dokumen_invoice_url,
            user_id=current_user_id
            )

        return await self.repo.create_dokumen_invoice(dokumen_invoice_form)
    
    async def lists_all_dokumen_invoice(self):
        return await self.repo.get_all_dokumen_invoice()
    
    async def get_all_dokumen_invoice_by_user_id(self, user_id: int):
        return await self.repo.get_all_dokumen_invoice_user(user_id=user_id)

    
    async def get_dokumen_invoice_by_id(self, dokumen_invoice_id: int):
        try:
            dokumen_invoice = await self.repo.get_dokumen_invoice_by_id(dokumen_invoice_id=dokumen_invoice_id)
            if not dokumen_invoice:
                logger.warning(f"[Service Warning][GET_BY_ID] Dokumen Invoice with id={dokumen_invoice_id} not found")
                raise HTTPException(status_code=404, detail="ID Dokumen Invoice Tidak Ditemukan")
            return dokumen_invoice
    
        except SQLAlchemyError as e:
            logger.error(f"[Service Error][GET_BY_ID] {str(e)}", exc_info=True)
            raise e
        except Exception as e:
            logger.error(f"[Service Unexpected Error][GET_BY_ID] {str(e)}", exc_info=True)
            raise e
        
    
    async def update_dokumen_invoice_by_id(self, form_id: int, data: dict, user_id: int):
        return await self.repo.update_dokumen_invoice(form_id, data, user_id)
    
    
    async def delete_dokumen_invoice_by_id(self, form_id: int):
        return await self.repo.delete_dokumen_invoice_by_id(form_id)
    
    # @root_validator
    # def check_other_service(cls, values):
    #     if values["insurance_type"] == "lainnya" and not values.get("other_service"):
    #         raise ValueError("other_service must be provided if insurance_type is 'lainnya'")
    #     return values