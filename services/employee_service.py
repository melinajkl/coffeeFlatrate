"""
employee_service.py

This module contains functions for managing employee records in the database,
including creation, retrieval, updating, and deletion. It uses SQLAlchemy ORM
and expects Pydantic schemas for data validation and transfer.

Functions:
- create_employee
- get_employee
- get_all_employees
- patch_employee
- delete_employee
"""
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.model import Employee
from schemas.employee import EmployeeCreate, EmployeeOut, EmployeeDelete
from utils.security import hash_password

def create_employee(db: Session, data: EmployeeCreate) -> Employee:
    """
    Creates a new employee and stores it in the database.

    Args:
        db (Session): The SQLAlchemy database session.
        data (EmployeeCreate): The data required to create a new employee.

    Returns:
        Employee: The created Employee ORM model instance.
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
    Retrieves a single employee by cafe ID and employee ID.

    Args:
        cafe_id (str): The ID of the café the employee belongs to.
        id (str): The ID of the employee.
        db (Session): The SQLAlchemy database session.

    Returns:
        EmployeeOut: The matching employee or None if not found.
    """
    return db.query(Employee).filter(
        and_(
            Employee.cafe_id == cafe_id,
            Employee.id == id
        )
    ).first()


def get_all_employees(cafe_id: str, db: Session) -> List[EmployeeOut]:
    """
    Retrieves all employees associated with a specific café.

    Args:
        cafe_id (str): The ID of the café.
        db (Session): The SQLAlchemy database session.

    Returns:
        List[EmployeeOut]: A list of employees for the given café.
    """
    return db.query(Employee).filter(Employee.cafe_id == cafe_id).all()


def patch_employee(model: EmployeeCreate, db: Session) -> EmployeeOut:
    """
    Updates an existing employee's information.

    Args:
        model (EmployeeCreate): The updated employee data.
        db (Session): The SQLAlchemy database session.

    Returns:
        EmployeeOut: The updated employee record.
    """
    emp = db.query(Employee).filter(
        and_(
            Employee.cafe_id == model.cafe_id,
            Employee.id == model.id
        )
    ).first()
    if not emp:
        raise HTTPException(404, "User not found")
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
        emp (EmployeeDelete): Contains the café ID and employee ID to identify the employee.
        db (Session): The SQLAlchemy database session.

    Returns:
        dict: A message confirming the deletion.
    """
    db_model = get_employee(emp.cafe_id, emp.id, db)
    db.delete(db_model)
    db.commit()
    return {"message": f"Eintrag mit der id {emp.id} wurde erfolgreich gelöscht"}
