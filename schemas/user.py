from pydantic import BaseModel, EmailStr, Field
from utils import csv_storage

class UserCreate(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    abo_id: int = Field(..., gt=0)
    paid: bool = False