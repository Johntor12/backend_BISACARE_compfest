from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DokumenInvoice(BaseModel):
    dokumen_invoice_id: int | None = None
    dokumen_invoice_url: str

    created_at: datetime = datetime.now()
    user_id: int