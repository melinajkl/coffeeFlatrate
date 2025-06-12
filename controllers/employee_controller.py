from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.employee import EmployeeCreate, EmployeeOut
from services import employee_service
from database import get_db

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/", response_model=EmployeeOut)
def register_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return employee_service.create_employee(db, employee)
