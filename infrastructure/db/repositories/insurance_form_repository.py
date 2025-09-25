from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.db.models.insurance_form_model import InsuranceFormModel
from domain.entities.insurance_form import InsuranceForm
import logging
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import Optional, List, Dict
from schemas.insurance_form_schema import InsuranceFormResponse, InsuranceFormRequest
from datetime import datetime


logger = logging.getLogger(__name__)

class InsuranceFormRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_insurance_form(self, form: InsuranceFormModel) -> InsuranceFormModel:
        try:
            self.db.add(form)
            await self.db.commit()
            await self.db.refresh(form)
            return form
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"[Repository Error][CREATE] {str(e)}", exc_info=True)
            raise e

    async def get_all_insurance_form(self) -> List[InsuranceFormModel]:
        try:
            result = await self.db.execute(select(InsuranceFormModel))
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"[Repository Error][GET_ALL] {str(e)}", exc_info=True)
            raise e


    async def get_insurance_form_by_id(self, form_id: int) -> Optional[InsuranceFormModel]:
        try:
            result = await self.db.execute(
                select(InsuranceFormModel)
                .where(InsuranceFormModel.form_id==form_id)
            )

            return result.scalars().first()
        
        except SQLAlchemyError as e:
            logger.error(f"[Repository Error][GET_BY_ID] {str(e)}", exc_info=True)
            raise e
        
    

    async def update_insurance_form_by_id(self, form_id: int, update_data: dict, ktp_url: Optional[str] = None, insurance_card_url: Optional[str] = None) -> Optional[InsuranceFormModel]:
        try:

            if(ktp_url):
                InsuranceForm["ktp_url"] = ktp_url
            if(insurance_card_url):
                InsuranceForm["insurance_card_url"] = insurance_card_url

            await self.db.execute(
                update(InsuranceFormModel)
                .where(InsuranceFormModel.form_id==form_id)
                .values(**update_data,
                        )
            )
            await self.db.commit()
            return await self.get_insurance_form_by_id(form_id)

        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"[Repository Error][UPDATE] {str(e)}", exc_info=True)
            raise e

    async def delete_insurance_form_by_id(self, form_id: int):
        try:
            form = await self.get_insurance_form_by_id(form_id)
            if form:
                self.db.delete(form)
                await self.db.commit()
            return {"msg": "Insurance Form berhasil dihapus"}
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"[Repository Error][DELETE] {str(e)}", exc_info=True)
            raise e