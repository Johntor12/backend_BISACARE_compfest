from dataclasses import dataclass
from datetime import datetime

class ClaimDocument:
    id: int | None
    claim_id: int
    document_name: str
    document_url: str
    uploaded_at: datetime