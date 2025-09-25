from infrastructure.db.repositories.aju_banding_repository import AjuBandingRepository
from infrastructure.storage.supabase_storage import SupabaseStorage
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.aju_banding import AjuBanding
from schemas.aju_banding_schema import AjuBandingRequest, AjuBandingResponse
from infrastructure.db.models.aju_banding_model import AjuBandingModel
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

class AjuBandingService:
    def __init__(self, session: AsyncSession, storage: SupabaseStorage):
        self.repo = AjuBandingRepository(session)
        self.storage = storage


    async def save_file(self, file: UploadFile, prefix:str) -> str:
        ext = os.path.split(file.filename)[1]
        filename = f"{prefix}_{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return filename

    async def create_aju_banding(self, aju_banding: Optional[UploadFile], current_user_id: int ) -> AjuBanding:
        
        # Upload file ke Supabase
        aju_banding_url = await self.storage.upload_file(aju_banding, "aju_banding") if aju_banding else None
        
        aju_banding_form = AjuBanding(
            aju_banding_url=aju_banding_url,
            user_id=current_user_id
            )

        return await self.repo.create_aju_banding(aju_banding_form)
    
    async def lists_all_aju_banding(self):
        return await self.repo.get_all_aju_banding()
    
    async def get_all_aju_banding_by_user_id(self, user_id: int):
        return await self.repo.get_all_aju_banding_user(user_id)

    
    async def get_aju_banding_by_id(self, aju_banding_id: int):
        aju_banding = await self.repo.get_aju_banding_by_id(aju_banding_id)
        if not aju_banding:
            logger.warning(f"[Service Warning][GET_BY_ID] Insurance form with id={aju_banding_id} not found")
            raise HTTPException(status_code=404, detail="ID Form Tidak Ditemukan")
        return aju_banding
        
    
    async def update_aju_banding_by_id(self, form_id: int, data: dict, user_id: int):
        return await self.repo.update_aju_banding(form_id, data, user_id)
    
    
    async def delete_aju_banding_by_id(self, form_id: int):
        return await self.repo.delete_aju_banding_by_id(form_id)
    
    # @root_validator
    # def check_other_service(cls, values):
    #     if values["insurance_type"] == "lainnya" and not values.get("other_service"):
    #         raise ValueError("other_service must be provided if insurance_type is 'lainnya'")
    #     return values