from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, Any

class CustomerCreate(BaseModel):
    name: str
    password: str
    email: EmailStr
    paymentMethod: int

class CustomerOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    drinksDrunk: int
    lastPaid: Optional[date]

    class Config:
        orm_mode = True

class CustomerStats(BaseModel):
    name: str
    email: EmailStr
    drinksDrunk: int 
    drinkLog: Any
    activated: bool