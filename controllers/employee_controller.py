"""
This module defines routes for managing employees in the CoffeeClub system.

Endpoints:
- POST /employees/: Register a new employee
- GET /employees/{cafe_id}/employee/{id}: Get a specific employee by composite key
- GET /employees/{id}/employees: Get all employees of a café
- PATCH /employees/: Update an employee
- DELETE /employees/: Delete an employee
- POST /employees/login: Authenticate an employee and return a JWT token

All actions (except login) require DB session injection. Authentication is handled via auth_service.
"""

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
        db (Session): SQLAlchemy session for database operations.

    Returns:
        EmployeeOut: Created employee data without password.
    """
    return employee_service.create_employee(db, employee)


@router.get("/{cafe_id}/employee/{id}")
def get_employee(cafe_id: str, id: str, db: Session = Depends(get_db)):
    """
    Retrieve a single employee using the composite key (café ID + employee ID).

    Args:
        cafe_id (str): ID of the café.
        id (str): ID of the employee.

    Returns:
        dict: Full employee information.
    """
    return employee_service.get_employee(cafe_id, id, db)


@router.get("/{id}/employees", response_model=List[EmployeeOut])
def get_all_emp(id: str, db: Session = Depends(get_db)):
    """
    Get all employees working at a specific café.

    Args:
        id (str): Café ID.

    Returns:
        List[EmployeeOut]: List of employees registered at the café.
    """
    return employee_service.get_all_employees(id, db)


@router.patch("/", response_model=EmployeeOut)
def patch_emp(model: EmployeeCreate, db: Session = Depends(get_db)):
    """
    Update employee data.

    Args:
        model (EmployeeCreate): Updated employee information.
        db (Session): SQLAlchemy session for database operations.

    Returns:
        EmployeeOut: The updated employee data.
    """
    return employee_service.patch_employee(model, db)


@router.delete("/")
def delete_emp(emp: EmployeeDelete, db: Session = Depends(get_db)):
    """
    Delete an employee using the composite key (café ID + employee ID).

    Args:
        emp (EmployeeDelete): Identifiers for the employee to be deleted.
        db (Session): SQLAlchemy session for database operations.

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
    Authenticate an employee and return a JWT access token.

    Args:
        employee_id (str): Unique employee ID.
        cafe_id (str): Café ID the employee belongs to.
        password (str): Plaintext password.
        db (Session): SQLAlchemy session for authentication.

    Returns:
        Token: JWT access token and type.
    """
    token = auth_service.authenticate_employee(db, employee_id, cafe_id, password)
    return {"access_token": token, "token_type": "bearer"}
