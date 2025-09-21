# domain/entities/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: int | None = None
    username: str
    email: EmailStr
    password: str
    nomor_telepon: str
    insurance_form_id: Optional[int] | None = None
    slip_id: Optional[int] | None = None