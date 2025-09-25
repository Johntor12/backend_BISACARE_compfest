
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, File , Form
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.repositories.dokumen_invoice_repository import DokumenInvoiceRepository
from application.usecases.dokumen_invoice_services import DokumenInvoiceService
from application.usecases.helper.get_current_user_service import get_current_user_service
from schemas.dokumen_invoice_schema import DokumenInvoiceRequest, DokumenInvoiceResponse
from infrastructure.db.connection import get_db
from infrastructure.storage.supabase_storage import SupabaseStorage
from domain.entities.insurance_form import InsuranceForm
from datetime import datetime
import os

router = APIRouter(tags=["Dokumen Invoice"])
UPLOAD_DIR  = "uploads/insurance_forms"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=DokumenInvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_dokumen_invoice(db: AsyncSession = Depends(get_db), dokumen_invoice: UploadFile = File(None), current_user = Depends(get_current_user_service)):
    storage = SupabaseStorage()
    service = DokumenInvoiceService(db, storage)

    try:
        created = await service.create_dokumen_invoice(dokumen_invoice=dokumen_invoice, current_user_id=current_user.id)
        return created
    except Exception as e:
        # log and return 500
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/")
async def list_dokumen_invoices(db: AsyncSession = Depends(get_db)):
    storage = SupabaseStorage()
    service = DokumenInvoiceService(db, storage)
    return await service.lists_all_dokumen_invoice()

@router.get("/{user_id}")
async def list_user_dokumen_invoices(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user_service)):
    storage = SupabaseStorage()
    service = DokumenInvoiceService(db, storage)
    return await service.get_all_dokumen_invoice_by_user_id(user_id=current_user.id)

@router.get("/{dokumen_invoice_id}")
async def get_dokumen_invoice(dokumen_invoice_id: int, db: AsyncSession = Depends(get_db)):
    storage = SupabaseStorage()
    service = DokumenInvoiceService(db, storage)
    return await service.get_dokumen_invoice_by_id(dokumen_invoice_id=dokumen_invoice_id)

@router.put("/{dokumen_invoice_id}")
async def update_dokumen_invoice(dokumen_invoice_id: int, dokumen_invoice_url: UploadFile = File(None), db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user_service)):
    storage = SupabaseStorage()
    service = DokumenInvoiceService(db, storage)
    return await service.update_dokumen_invoice_by_id(dokumen_invoice_id, dokumen_invoice_url, current_user.id)

@router.delete("/{dokumen_invoice_id}")
async def delete_dokumen_invoice(dokumen_invoice_id: int, db: AsyncSession = Depends(get_db)):
    storage = SupabaseStorage()
    service = DokumenInvoiceService(db, storage)
    return await service.delete_dokumen_invoice_by_id(dokumen_invoice_id)

@router.get("/{dokumen_invoice_id}/file")
async def get_dokumen_invoice_file_url(dokumen_invoice_id: int, db: AsyncSession = Depends(get_db)):
    """
    file_type: 'ktp' or 'insurance_card'
    returns stored URL (public) or signed URL if you choose private.
    """
    repo = DokumenInvoiceRepository(db)
    model = await repo.get_dokumen_invoice_by_id(dokumen_invoice_id=dokumen_invoice_id)
    if not model:
        raise HTTPException(status_code=404, detail="Aju Banding not found")
    return model.dokumen_invoice_url