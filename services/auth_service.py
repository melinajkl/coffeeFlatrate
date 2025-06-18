"""
auth_service.py

Handles authentication logic for employees and customers.
Verifies credentials and generates JWT access tokens upon successful login.
"""

from sqlalchemy import and_
from sqlalchemy.orm import Session
from pydantic import EmailStr
from fastapi import HTTPException
from models.model import Employee, Customer
from utils.security import verify_password, create_access_token

def authenticate_employee(db: Session, employee_id: str, cafe_id: str, password: str) -> str:
    """
    Authenticates an employee using their ID, café ID, and password.

    Args:
        db (Session): SQLAlchemy database session.
        employee_id (str): The ID of the employee.
        cafe_id (str): The ID of the café the employee belongs to.
        password (str): The plain text password to verify.

    Raises:
        HTTPException: If the employee does not exist or the password is invalid.

    Returns:
        str: JWT access token containing employee credentials.
    """
    employee = db.query(Employee).filter(
        and_(
            Employee.id == employee_id,
            Employee.cafe_id == cafe_id
        )
    ).first()

    if not employee or not verify_password(password, employee.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {
        "sub": employee.id,
        "cafe_id": employee.cafe_id,
        "sudo": employee.sudo
    }

    return create_access_token(token_data)


def authenticate_customer(db: Session, emailS: EmailStr, password: str) -> str:
    """
    Authenticates a customer using their email and password.

    Args:
        db (Session): SQLAlchemy database session.
        emailS (EmailStr): The customer's email address.
        password (str): The plain text password to verify.

    Raises:
        HTTPException: If the customer does not exist or the password is invalid.

    Returns:
        str: JWT access token containing customer information.
    """
    customer = db.query(Customer).filter(emailS == Customer.email).first()
    
    if not customer or not verify_password(password, customer.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {
        "id": customer.id,
        "name": customer.name,
        "drinksdrunk": customer.drinksDrunk
    }

    return create_access_token(token_data)