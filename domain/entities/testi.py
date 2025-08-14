from pydantic import BaseModel
from typing import Optional

class Testi(BaseModel):
    testi_id: Optional[int]
    source_person: str
    image_person: str
    testi: str