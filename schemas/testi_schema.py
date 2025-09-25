from pydantic import BaseModel
from typing import Optional

class TestiRequest(BaseModel):
    source_person: str
    image_person: str
    testi: str

class TestiResponse(BaseModel):
    source_person: str
    image_person: str
    testi: str