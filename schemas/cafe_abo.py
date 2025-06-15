from pydantic import BaseModel

class AboCafeBase(BaseModel):
    cafe_id: str
    abo_id: str
    
class AboCafeCreate(AboCafeBase):
    pass