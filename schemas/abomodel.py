from pydantic import BaseModel, EmailStr

class AboModelBase(BaseModel):
    id: str
    specialdrinks: bool
    priceperweek: int
    amount: int
    
    class Config:
        orm_mode = True
        
class AboModelCreate(AboModelBase):
    pass