from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.db.models.insurance_form_model import InsuranceFormModel
from domain.entities.insurance_form import InsuranceForm
import logging
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import Optional, List, Dict
from schemas.insurance_form_schema import InsuranceFormResponse
from datetime import datetime


logger = logging.getLogger(__name__)

class InsuranceFormRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_insurance_form(self, db_form: InsuranceForm):
        try:
            new_db_form = InsuranceFormModel(
                ktp_url=db_form.ktp_url,
                insurance_card_url=db_form.insurance_card_url,
                policy_number=db_form.policy_number,
                rekening_type=db_form.rekening_type,
                rekening_number=db_form.rekening_number,
                service_type=db_form.service_type,
                other_service=db_form.other_service,
                phone_number=db_form.phone_number,
                complaint=db_form.complaint,
                created_at=datetime.now(),
            )
            self.db.add(new_db_form)
            await self.db.commit()
            await self.db.refresh(db_form)
            return db_form
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

    async def update_insurance_form_by_id(self, form_id: int, update_data: dict):
        try:
            await self.db.execute(
                update(InsuranceFormModel)
                .where(InsuranceFormModel.form_id==form_id)
                .values(**update_data)
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
            return form
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"[Repository Error][DELETE] {str(e)}", exc_info=True)
            raise e