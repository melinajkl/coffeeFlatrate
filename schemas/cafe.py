from pydantic import BaseModel, EmailStr, Field
from typing import List

class CafeCreate(BaseModel):
    id: str
    iban: str
    bic: str
    account_holder: str
    abolist: List[str] #list of abomodel ids