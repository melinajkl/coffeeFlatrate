from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from schemas.token import Token
from schemas.employee import EmployeeCreate, EmployeeOut, EmployeeDelete
from services import employee_service, auth_service
from database import get_db
from typing import List

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/", response_model=EmployeeOut)
def register_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return employee_service.create_employee(db, employee)

@router.get("/{cafe_id}/employee/{id}")
def get_employee(cafe_id: str, id: str, db: Session = Depends(get_db)):
    return employee_service.get_employee(cafe_id, id, db)

@router.get("/{id}/employees", response_model = List[EmployeeOut])
def get_all_emp(id: str, db: Session = Depends(get_db)):
    return employee_service.get_all_employees(id, db)

@router.patch("/", response_model=EmployeeOut)
def patch_emp(model: EmployeeCreate, db: Session = Depends(get_db)):
    return employee_service.patch_employee(model, db)

@router.delete("/")
def delete_emp(emp: EmployeeDelete, db: Session = Depends(get_db)):
    return employee_service.delete_employee(emp, db)

@router.post("/login", response_model=Token)
def login(
    employee_id: str = Form(...),
    cafe_id: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    token = auth_service.authenticate_employee(db, employee_id, cafe_id, password)
    return {"access_token": token, "token_type": "bearer"}