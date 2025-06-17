"""
employee_service.py

This module provides database operations for managing employee records using SQLAlchemy.
It includes functions for creating, retrieving, updating, and deleting employee entries.
Password hashing is performed via a utility function before storing credentials securely.
The module relies on Pydantic schemas for request/response validation and structure.

Functions:
- create_employee: Add a new employee to the database.
- get_employee: Retrieve a single employee by café and ID.
- get_all_employees: List all employees of a specific café.
- patch_employee: Update an existing employee's information.
- delete_employee: Remove an employee from the database.
"""
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.model import Employee
from schemas.employee import EmployeeCreate, EmployeeOut, EmployeeDelete
from utils.security import hash_password

def create_employee(db: Session, data: EmployeeCreate) -> Employee:
    """
    Creates a new employee and stores it in the database.

    Args:
        db (Session): The database session.
        data (EmployeeCreate): Pydantic model containing employee input data.

    Returns:
        Employee: The newly created employee ORM object.
    """
    db_employee = Employee(
        id=data.id,
        name=data.name,
        hashed_password=hash_password(data.password),
        sudo=data.sudo,
        cafe_id=data.cafe_id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def get_employee(cafe_id: str, id: str, db: Session) -> EmployeeOut:
    """
    Retrieves a single employee by their café ID and employee ID.

    Args:
        cafe_id (str): The café identifier.
        id (str): The employee's ID.
        db (Session): The database session.

    Returns:
        EmployeeOut: The employee if found, otherwise None.
    """
    return db.query(Employee).filter(
        and_(
            Employee.cafe_id == cafe_id,
            Employee.id == id
        )
    ).first()


def get_all_employees(cafe_id: str, db: Session) -> List[EmployeeOut]:
    """
    Retrieves all employees belonging to a specific café.

    Args:
        cafe_id (str): The café identifier.
        db (Session): The database session.

    Returns:
        List[EmployeeOut]: A list of all matching employees.
    """
    return db.query(Employee).filter(Employee.cafe_id == cafe_id).all()


def patch_employee(model: EmployeeCreate, db: Session) -> EmployeeOut:
    """
    Updates the details of an existing employee.

    Args:
        model (EmployeeCreate): The updated employee data.
        db (Session): The database session.

    Returns:
        EmployeeOut: The updated employee object.
    """
    emp = db.query(Employee).filter(
        and_(
            Employee.cafe_id == model.cafe_id,
            Employee.id == model.id
        )
    ).first()
    emp.name = model.name
    emp.sudo = model.sudo
    emp.hashed_password = hash_password(model.password)
    db.commit()
    db.refresh(emp)
    return emp


def delete_employee(emp: EmployeeDelete, db: Session) -> dict:
    """
    Deletes an employee from the database.

    Args:
        emp (EmployeeDelete): Pydantic model with café ID and employee ID.
        db (Session): The database session.

    Returns:
        dict: A confirmation message after successful deletion.
    """
    db_model = get_employee(emp.cafe_id, emp.id, db)
    db.delete(db_model)
    db.commit()
    return {"message": f"Eintrag mit der id {emp.id} wurde erfolgreich gelöscht"}
