from typing import List
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from schemas.token import Token
from schemas.employee import EmployeeCreate, EmployeeOut, EmployeeDelete
from services import employee_service, auth_service
from database import get_db

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/", response_model=EmployeeOut)
def register_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """
    Register a new employee for a specific café.

    Args:
        employee (EmployeeCreate): Employee registration data.
        db (Session): Database session (injected).

    Returns:
        EmployeeOut: Data of the created employee (excluding password).
    """
    return employee_service.create_employee(db, employee)

@router.get("/{cafe_id}/employee/{id}")
def get_employee(cafe_id: str, id: str, db: Session = Depends(get_db)):
    """
    Retrieve a single employee by café ID and employee ID (composite key).

    Args:
        cafe_id (str): ID of the café.
        id (str): ID of the employee.

    Returns:
        dict: Full employee data (optional - consider limiting fields).
    """
    return employee_service.get_employee(cafe_id, id, db)

@router.get("/{id}/employees", response_model=List[EmployeeOut])
def get_all_emp(id: str, db: Session = Depends(get_db)):
    """
    Get all employees of a specific café.

    Args:
        id (str): Café ID.

    Returns:
        List[EmployeeOut]: List of employees for the café.
    """
    return employee_service.get_all_employees(id, db)

@router.patch("/", response_model=EmployeeOut)
def patch_emp(model: EmployeeCreate, db: Session = Depends(get_db)):
    """
    Update an existing employee's data (except password unless handled inside).

    Args:
        model (EmployeeCreate): New employee data to apply.

    Returns:
        EmployeeOut: Updated employee information.
    """
    return employee_service.patch_employee(model, db)

@router.delete("/")
def delete_emp(emp: EmployeeDelete, db: Session = Depends(get_db)):
    """
    Delete an employee using ID and café ID.

    Args:
        emp (EmployeeDelete): Composite key to identify the employee.

    Returns:
        dict: Confirmation message.
    """
    return employee_service.delete_employee(emp, db)

@router.post("/login", response_model=Token)
def login(
    employee_id: str = Form(...),
    cafe_id: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Authenticate an employee and return an access token.

    Args:
        employee_id (str): ID of the employee.
        cafe_id (str): Café ID for context.
        password (str): Plaintext password.

    Returns:
        Token: JWT access token and type.
    """
    token = auth_service.authenticate_employee(db, employee_id, cafe_id, password)
    return {"access_token": token, "token_type": "bearer"}
