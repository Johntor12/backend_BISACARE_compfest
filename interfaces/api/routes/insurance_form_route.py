
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.repositories.insurance_form_repository import InsuranceFormRepository
from application.usecases.insurance__form_services import InsuranceFormService
from schemas.insurance_form_schema import InsuranceFormRequest
from infrastructure.db.connection import get_db
from domain.entities.insurance_form import InsuranceForm
from datetime import datetime

router = APIRouter(prefix="/insuranceform", tags=["Insurance_Form"])

@router.post("/", response_model=dict)
async def create_form(req: InsuranceFormRequest, db: AsyncSession = Depends(get_db)):
    repo = InsuranceFormRepository(db)
    service = InsuranceFormService(repo)
    try:
        form = InsuranceForm(
            id=None,
            ktp_url=req.ktp_url,
            insurance_card_url=req.insurance_card_url,
            policy_number=req.policy_number,
            service_type=req.service_type,
            other_service=req.other_service,
            phone_number=req.phone_number,
            complaint=req.complaint,
            created_at=datetime.now()
        )
        result = await service.create_form(form)
        return {"message": "Form created successfully", "data": result.model_dump()}

    except Exception as err:
        print(f'Error creating form: {err}')
        raise HTTPException(status_code=500, detail=str(err))


    

@router.get("/")
async def list_forms(db: AsyncSession = Depends(get_db)):
    repo = InsuranceFormRepository(db)
    service = InsuranceFormService(repo)
    return await service.lists_all_forms()

@router.get("/{form_id}")
async def get_form(form_id: int, db: AsyncSession = Depends(get_db)):
    repo = InsuranceFormRepository(db)
    service = InsuranceFormService(repo)
    return await service.get_form_by_id(form_id)

@router.put("/{form_id}")
async def update_form(form_id: int, req: InsuranceFormRequest, db: AsyncSession = Depends(get_db)):
    repo = InsuranceFormRepository(db)
    service = InsuranceFormService(repo)
    return await service.update_form_by_id(form_id, req.dict())

@router.delete("/{form_id}")
async def delete_form(form_id: int, db: AsyncSession = Depends(get_db)):
    repo = InsuranceFormRepository(db)
    service = InsuranceFormService(repo)
    return await service.delete_form_by_id(form_id)