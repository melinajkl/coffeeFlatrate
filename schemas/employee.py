from pydantic import BaseModel, EmailStr, Field

class EmployeeCreate(BaseModel):
    name : str 
    password: str
    sudo: bool = False
    cafe_id: str #Link to a Café
    
class EmployeeOut(BaseModel):
    id: str
    name: str
    sudo: bool
    cafe_id: str
    
    class Config:
        orm_mode = True