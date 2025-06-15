from pydantic import BaseModel
from typing import List

from pydantic import BaseModel, field_validator
from typing import List
from utils.validation import validate_iban_format, validate_bic_format  # adjust import path

class CafeCreate(BaseModel):
    id: str
    iban: str
    bic: str
    account_holder: str
    abomodels: List[str]

    @field_validator("iban")
    def validate_iban(cls, v):
        if not validate_iban_format(v):
            raise ValueError("Invalid IBAN format")
        return v.replace(" ", "").upper()

    @field_validator("bic")
    def validate_bic(cls, v):
        if not validate_bic_format(v):
            raise ValueError("Invalid BIC format")
        return v.upper()


class CafeOut(BaseModel):
    id: str
    iban: str
    bic: str
    account_holder: str

    class Config:
        orm_mode = True
        
class CafeOutB(BaseModel):
    id: str
    iban: str
    bic: str
    account_holder: str
    abomodels: List[str]  # oder List[AboModelOut], falls du Details willst

    class Config:
        orm_mode = True