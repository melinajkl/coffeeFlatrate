from pydantic import BaseModel, EmailStr, Field

class EmployeeCreate(BaseModel):
    id : str
    name : str 
    password: str
    sudo: bool = False
    cafe_id: str #Link to a Café
    
class EmployeeOut(BaseModel):
    id: str
    name: str
    sudo: bool
    
    class Config:
        orm_mode = True
        
class EmployeeDelete(BaseModel):
    id: str
    cafe_id: str