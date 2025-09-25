from infrastructure.db.repositories.insurance_form_repository import InsuranceFormRepository
from infrastructure.storage.supabase_storage import SupabaseStorage
from domain.entities.insurance_form import InsuranceForm
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.insurance_form_schema import InsuranceFormResponse, InsuranceFormRequest
from infrastructure.db.models.insurance_form_model import InsuranceFormModel
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

class InsuranceFormService:
    def __init__(self, session: AsyncSession, storage: SupabaseStorage):
        self.repo = InsuranceFormRepository(session)
        self.storage = storage


    async def save_file(self, file: UploadFile, prefix:str) -> str:
        ext = os.path.split(file.filename)[1]
        filename = f"{prefix}_{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return filename

    async def create_form(self, request: InsuranceFormRequest, ktp: Optional[UploadFile], insurance_card: Optional[UploadFile]):
        
        # Upload file ke Supabase
        ktp_url = await self.storage.upload_file(ktp, "ktp") if ktp else None
        insurance_card_url = await self.storage.upload_file(insurance_card, "insurance_card") if insurance_card else None

        form = InsuranceFormModel(
            **request.dict(),
            ktp_url=ktp_url,
            insurance_card_url=insurance_card_url,
        )
        return await self.repo.create_insurance_form(form)
    
    async def lists_all_forms(self):
        return await self.repo.get_all_insurance_form()
    
    async def get_form_by_id(self, form_id: int):
        try:
            insurance_form = await self.repo.get_insurance_form_by_id(form_id)
            if not insurance_form:
                logger.warning(f"[Service Warning][GET_BY_ID] Insurance form with id={form_id} not found")
                raise HTTPException(status_code=404, detail="ID Form Tidak Ditemukan")
            return insurance_form
        except SQLAlchemyError as e:
            logger.error(f"[Service Error][GET_BY_ID] {str(e)}", exc_info=True)
            raise e
        except Exception as e:
            logger.error(f"[Service Unexpected Error][GET_BY_ID] {str(e)}", exc_info=True)
            raise e
    
    async def update_form_by_id(self, form_id: int, data: InsuranceFormRequest, ktp: Optional[UploadFile], insurance_card: Optional[UploadFile]):
        ktp_url = await self.storage.upload_file(ktp, "ktp") if ktp else None
        insurance_card_url = await self.storage.upload_file(insurance_card, "insurance_card") if insurance_card else None

        update_dict = data.dict(exclude_unset=True)
        updated = await self.repo.update_insurance_form_by_id(form_id, update_dict, ktp_url, insurance_card_url)
        if not updated:
            raise HTTPException(status_code=404, detail="ID Form tidak ditemukan")
        return InsuranceFormResponse.from_orm(updated)
    
    async def delete_form_by_id(self, form_id: int):
        return await self.repo.delete_insurance_form_by_id(form_id)
    
    # @root_validator
    # def check_other_service(cls, values):
    #     if values["insurance_type"] == "lainnya" and not values.get("other_service"):
    #         raise ValueError("other_service must be provided if insurance_type is 'lainnya'")
    #     return values