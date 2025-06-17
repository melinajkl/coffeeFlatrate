from pydantic import BaseModel, field_validator
from typing import List
from utils.validation import validate_iban_format, validate_bic_format  # adjust import path

class CafeCreate(BaseModel):
    """
    Schema for creating a new café, with validation for IBAN and BIC.

    Attributes:
        id (str): Unique ID of the café.
        iban (str): IBAN of the bank account, validated and formatted.
        bic (str): BIC of the bank account, validated and formatted.
        account_holder (str): Name of the account holder.
        abomodels (List[str]): List of AboModel IDs assigned to the café.
    """

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
    """
    Output schema for café data without AboModel details.

    Attributes:
        id (str): Unique ID of the café.
        iban (str): IBAN of the bank account.
        bic (str): BIC of the bank account.
        account_holder (str): Name of the account holder.
    """

    id: str
    iban: str
    bic: str
    account_holder: str

    class Config:
        orm_mode = True


class CafeOutB(BaseModel):
    """
    Output schema for café data including associated AboModel IDs.

    Attributes:
        id (str): Unique ID of the café.
        iban (str): IBAN of the bank account.
        bic (str): BIC of the bank account.
        account_holder (str): Name of the account holder.
        abomodels (List[str]): List of associated AboModel IDs.
    """

    id: str
    iban: str
    bic: str
    account_holder: str
    abomodels: List[str]  # Optionally: List[AboModelOut] if full model details are needed

    class Config:
        orm_mode = True
