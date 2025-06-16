from sqlalchemy import and_
from fastapi import HTTPException
from models.model import Employee, Customer
from utils.security import verify_password, create_access_token
from sqlalchemy.orm import Session
from pydantic import EmailStr

def authenticate_employee(db: Session, employee_id: str, cafe_id: str, password: str) -> str:
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

def authenticate_customer(db: Session, emailS: EmailStr, password:str):
    customer = db.query(Customer).filter(emailS == Customer.email).first()
    if not customer or not verify_password(password, customer.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token_data = {
        "id": customer.id,
        "name": customer.name,
        "drinksdrunk": customer}
    
    return create_access_token(token_data)