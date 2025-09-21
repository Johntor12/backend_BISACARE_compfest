from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.db.models.insurance_form_model import InsuranceFormModel
from domain.entities.insurance_form import InsuranceForm
import logging
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import Optional, List, Dict
from schemas.insurance_form_schema import InsuranceFormResponse


logger = logging.getLogger(__name__)

class InsuranceFormRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_insurance_form(self, form: InsuranceForm) -> InsuranceFormModel:
        try:
            db_form = InsuranceFormModel(
                ktp_url=form.ktp_url,
                insurance_card_url=form.insurance_card_url,
                policy_number=form.policy_number,
                rekening_type=form.rekening_type,
                rekening_number=form.rekening_number,
                service_type=form.service_type,
                other_service=form.other_service,
                phone_number=form.phone_number,
                complaint=form.complaint,
                created_at=form.created_at
            )
            self.db.add(db_form)
            await self.db.commit()
            await self.db.refresh(db_form)
            return db_form
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"[Repository Error][CREATE] {str(e)}", exc_info=True)
            raise e


    async def get_all_insurance_form(self) -> List[InsuranceFormResponse]:
        try:
            result = await self.db.execute(select(InsuranceFormModel))
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"[Repository Error][GET_ALL] {str(e)}", exc_info=True)
            raise e


    async def get_insurance_form_by_id(self, form_id: int) -> Optional[InsuranceFormResponse]:
        try:
            result = await self.db.execute(
                select(InsuranceFormModel)
                .where(InsuranceFormModel.form_id==form_id)
            )

            return result.scalars().first()
        
        except SQLAlchemyError as e:
            logger.error(f"[Repository Error][GET_BY_ID] {str(e)}", exc_info=True)
            raise e

    async def update_insurance_form_by_id(self, form_id: int, insuranceForm: dict) -> Optional[InsuranceFormResponse]:
        try:
            # kalau Pydantic model → jadikan dict
            if hasattr(insuranceForm, "dict"):
                update_data = insuranceForm.__dict__(exclude_unset=True)
            else:
                update_data = insuranceForm  # sudah dict

            await self.db.execute(
                update(InsuranceFormModel)
                .where(form_id==form_id)
                .values(update_data)
            )
            await self.db.commit()
            return await self.get_insurance_form_by_id(form_id)

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"[Repository Error][UPDATE] {str(e)}", exc_info=True)
            raise e

    def delete_insurance_form_by_id(self, form_id: int):
        try:
            form = self.get_insurance_form_by_id(form_id)
            if form:
                self.db.delete(form)
                self.db.commit()
            return form
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"[Repository Error][DELETE] {str(e)}", exc_info=True)
            raise e