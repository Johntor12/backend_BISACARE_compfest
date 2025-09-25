
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, File , Form
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.repositories.insurance_form_repository import InsuranceFormRepository
from application.usecases.insurance__form_services import InsuranceFormService
from application.usecases.helper.get_current_user_service import get_current_user_service
from schemas.insurance_form_schema import InsuranceFormRequest, InsuranceFormResponse
from infrastructure.db.connection import get_db
from infrastructure.storage.supabase_storage import SupabaseStorage
from domain.entities.insurance_form import InsuranceForm
from datetime import datetime
import os

router = APIRouter()
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
    current_user = Depends(get_current_user_service)
    ):
    storage = SupabaseStorage()
    service = InsuranceFormService(db, storage)
    
    req = InsuranceFormRequest(
        policy_number=policy_number,
        rekening_type=rekening_type,
        rekening_number=rekening_number,
        service_type=service_type,
        phone_number=phone_number,
        complaint=complaint,
        other_service=other_service,
        created_at=datetime.now(),
        user_id=current_user.id
    )
    try:
        created = await service.create_form(req, ktp_file, insurance_card_file)
        return created
    except Exception as e:
        # log and return 500
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    

@router.get("/")
async def list_forms(db: AsyncSession = Depends(get_db)):
    storage = SupabaseStorage()
    service = InsuranceFormService(db, storage)
    return await service.lists_all_forms()

@router.get("/{form_id}")
async def get_form(form_id: int, db: AsyncSession = Depends(get_db)):
    storage = SupabaseStorage()
    service = InsuranceFormService(db, storage)
    return await service.get_form_by_id(form_id)



@router.put("/{form_id}")
async def update_form(form_id: int,
                      policy_number: str = Form(...),
                        rekening_type: str = Form(...),
                        rekening_number: str = Form(...),
                        service_type: str = Form(...),
                        phone_number: str = Form(...),
                        complaint: str = Form(...),
                        other_service: str = Form(None),
                      db: AsyncSession = Depends(get_db), 
                      ktp_file: UploadFile = File(None),
                      insurance_card_file: UploadFile = File(None),
                      current_user = Depends(get_current_user_service)):
    storage = SupabaseStorage()
    service = InsuranceFormService(db, storage)
    
    req = InsuranceFormRequest(
        policy_number=policy_number,
        rekening_type=rekening_type,
        rekening_number=rekening_number,
        service_type=service_type,
        phone_number=phone_number,
        complaint=complaint,
        other_service=other_service,
        user_id=current_user
        )

    return await service.update_form_by_id(form_id, req, ktp_file, insurance_card_file)

@router.delete("/{form_id}")
async def delete_form(form_id: int, db: AsyncSession = Depends(get_db)):
    storage = SupabaseStorage()
    service = InsuranceFormService(db, storage)
    return await service.delete_form_by_id(form_id)

@router.get("/{form_id}/file/{file_type}")
async def get_file_url(form_id: int, file_type: str, db: AsyncSession = Depends(get_db)):
    """
    file_type: 'ktp' or 'insurance_card'
    returns stored URL (public) or signed URL if you choose private.
    """
    repo = InsuranceFormRepository(db)
    model = await repo.get_insurance_form_by_id(form_id)
    if not model:
        raise HTTPException(status_code=404, detail="Form not found")

    if file_type == "ktp":
        return {"url": model.ktp_url}
    elif file_type == "insurance_card":
        return {"url": model.insurance_card_url}
    else:
        raise HTTPException(status_code=400, detail="Unknown file type")