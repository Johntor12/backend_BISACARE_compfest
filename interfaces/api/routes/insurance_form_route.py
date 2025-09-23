
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, File , Form
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.repositories.insurance_form_repository import InsuranceFormRepository
from application.usecases.insurance__form_services import InsuranceFormService
from interfaces.api.routes.slip_route import get_current_user_id
from schemas.insurance_form_schema import InsuranceFormRequest, InsuranceFormResponse
from infrastructure.db.connection import get_db
from infrastructure.storage.supabase_storage import SupabaseStorage
from domain.entities.insurance_form import InsuranceForm
from datetime import datetime
import os

router = APIRouter(prefix="/insuranceform", tags=["Insurance_Form"])
UPLOAD_DIR  = "uploads/insurance_forms"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=InsuranceFormResponse, status_code=status.HTTP_201_CREATED)
async def create_form(
    policy_number: str = Form(...),
    rekening_type: str = Form(...),
    rekening_number: str = Form(...),
    service_type: str = Form(...),
    phone_number: str = Form(...),
    complaint: str = Form(...),
    other_service: str = Form(None),
    ktp_file: UploadFile = File(None),
    insurance_card_file: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
    ):
    repo = InsuranceFormRepository(db)
    storage = SupabaseStorage()
    service = InsuranceFormService(repo, storage)
    
    req = InsuranceFormRequest(
            policy_number=policy_number,
            service_type=service_type,
            other_service=other_service,
            rekening_type=rekening_type,
            rekening_number=rekening_number,
            phone_number=phone_number,
            complaint=complaint,
            created_at=datetime.now(),
            user_id=current_user_id
    )
    try:
        result = await service.create_form(req, ktp_file, insurance_card_file, current_user_id)    
        return {"message": "Form created successfully", "data": result}

    except Exception as err:
        print(f'Error creating form: {err}')
        raise HTTPException(status_code=500, detail=str(err))


    

@router.get("/")
async def list_forms(db: AsyncSession = Depends(get_db)):
    repo = InsuranceFormRepository(db)
    storage = SupabaseStorage()
    service = InsuranceFormService(repo, storage)
    return await service.lists_all_forms()

@router.get("/{form_id}")
async def get_form(form_id: int, db: AsyncSession = Depends(get_db)):
    repo = InsuranceFormRepository(db)
    storage = SupabaseStorage()
    service = InsuranceFormService(repo, storage)
    return await service.get_form_by_id(form_id)

@router.put("/{form_id}")
async def update_form(form_id: int, req: InsuranceFormRequest, db: AsyncSession = Depends(get_db)):
    repo = InsuranceFormRepository(db)
    storage = SupabaseStorage()
    service = InsuranceFormService(repo, storage)
    return await service.update_form_by_id(form_id, req.dict())

@router.delete("/{form_id}")
async def delete_form(form_id: int, db: AsyncSession = Depends(get_db)):
    repo = InsuranceFormRepository(db)
    storage = SupabaseStorage()
    service = InsuranceFormService(repo, storage)
    return await service.delete_form_by_id(form_id)