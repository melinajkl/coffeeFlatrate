from pydantic import BaseModel, EmailStr

class AboCreate(BaseModel):
    model_id: str
    cafe_id: str