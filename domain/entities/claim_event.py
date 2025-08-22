from dataclasses import dataclass
from datetime import datetime

class ClaimEvent:
    id: int | None
    claim_id: int
    event_type: int
    event_description: int
    event_date: datetime