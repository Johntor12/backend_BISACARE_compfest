from infrastructure.db.repositories.insurance_form_repository import InsuranceFormRepository
from domain.entities.insurance_form import InsuranceForm
from schemas.insurance_form_schema import InsuranceFormResponse
from sqlalchemy.exc import SQLAlchemyError
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class InsuranceFormService:
    def __init__(self, repo: InsuranceFormRepository):
        self.repo = repo

    async def create_form(self, form: InsuranceForm) -> InsuranceFormResponse:
        db_form = await self.repo.create_insurance_form(form)
        return InsuranceFormResponse.model_validate(db_form)
    
    async def lists_all_forms(self):
        return await self.repo.get_all_insurance_form()
    
    async def get_form_by_id(self, form_id: int):
        try:
            insurance_form = await self.repo.get_insurance_form_by_id(form_id)
            if not insurance_form:
                logger.warning(f"[Service Warning][GET_BY_ID] Insurance form with id={form_id} not found")
                return None
            return insurance_form
        except SQLAlchemyError as e:
            logger.error(f"[Service Error][GET_BY_ID] {str(e)}", exc_info=True)
            raise e
        except Exception as e:
            logger.error(f"[Service Unexpected Error][GET_BY_ID] {str(e)}", exc_info=True)
            raise e
    
    async def update_form_by_id(self, form_id: int, data: dict):
        return await self.repo.update_insurance_form_by_id(form_id, data)
    
    
    async def delete_form_by_id(self, form_id: int):
        return await self.repo.delete_insurance_form_by_id(form_id)
    
    # @root_validator
    # def check_other_service(cls, values):
    #     if values["insurance_type"] == "lainnya" and not values.get("other_service"):
    #         raise ValueError("other_service must be provided if insurance_type is 'lainnya'")
    #     return values