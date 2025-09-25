
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, File , Form
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.repositories.aju_banding_repository import AjuBandingRepository
from application.usecases.aju_banding_services import AjuBandingService
from application.usecases.helper.get_current_user_service import get_current_user_service
from schemas.aju_banding_schema import AjuBandingRequest, AjuBandingResponse
from infrastructure.db.connection import get_db
from infrastructure.storage.supabase_storage import SupabaseStorage
from domain.entities.insurance_form import InsuranceForm
from datetime import datetime
import os

router = APIRouter(tags=["Aju Banding"])
UPLOAD_DIR  = "uploads/insurance_forms"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=AjuBandingResponse, status_code=status.HTTP_201_CREATED)
async def create_aju_banding(db: AsyncSession = Depends(get_db), aju_banding: UploadFile = File(None), current_user = Depends(get_current_user_service)):
    storage = SupabaseStorage()
    service = AjuBandingService(db, storage)

    try:
        created = await service.create_aju_banding(aju_banding=aju_banding, current_user_id=current_user.id)
        return created
    except Exception as e:
        # log and return 500
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/")
async def list_aju_bandings(db: AsyncSession = Depends(get_db)):
    storage = SupabaseStorage()
    service = AjuBandingService(db, storage)
    return await service.lists_all_aju_banding()

@router.get("/{user_id}")
async def list_user_aju_bandings(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user_service)):
    storage = SupabaseStorage()
    service = AjuBandingService(db, storage)
    return await service.get_all_aju_banding_by_user_id(current_user.id)

@router.get("/{aju_banding_id}")
async def get_aju_banding(aju_banding_id: int, db: AsyncSession = Depends(get_db)):
    storage = SupabaseStorage()
    service = AjuBandingService(db, storage)
    return await service.get_aju_banding_by_id(aju_banding_id)

@router.put("/{aju_banding_id}")
async def update_aju_banding(aju_banding_id: int, aju_banding_url: UploadFile = File(None), db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user_service)):
    storage = SupabaseStorage()
    service = AjuBandingService(db, storage)
    return await service.update_aju_banding_by_id(aju_banding_id, aju_banding_url, current_user.id)

@router.delete("/{aju_banding_id}")
async def delete_aju_banding(aju_banding_id: int, db: AsyncSession = Depends(get_db)):
    storage = SupabaseStorage()
    service = AjuBandingService(db, storage)
    return await service.delete_aju_banding_by_id(aju_banding_id)

@router.get("/{aju_banding_id}/file")
async def get_aju_banding_file_url(aju_banding_id: int, db: AsyncSession = Depends(get_db)):
    """
    file_type: 'ktp' or 'insurance_card'
    returns stored URL (public) or signed URL if you choose private.
    """
    repo = AjuBandingRepository(db)
    model = await repo.get_aju_banding_by_id(aju_banding_id)
    if not model:
        raise HTTPException(status_code=404, detail="Aju Banding not found")
    return model.aju_banding_url