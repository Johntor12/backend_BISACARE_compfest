from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional

class DokumenInvoiceRequest(BaseModel):
    dokumen_invoice_url: str

class DokumenInvoiceResponse(BaseModel):
    id: int
    dokumen_invoice_url: str
    user_id: int
    created_at: datetime