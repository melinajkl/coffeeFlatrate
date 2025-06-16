from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.model import Employee
from models.functions import *
from schemas.employee import EmployeeCreate, EmployeeOut, EmployeeDelete
from utils.security import hash_password
from typing import List

def create_employee(db: Session, data: EmployeeCreate) -> Employee:
    db_employee = Employee(
        id = data.id,
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
    return db.query(Employee).filter(
        and_(
            Employee.cafe_id == cafe_id,
            Employee.id == id
        )
    ).first()

def get_all_employees(cafe_id: str, db: Session) -> List[EmployeeOut]:
    return db.query(Employee).filter(Employee.cafe_id == cafe_id).all()

def patch_employee( model: EmployeeCreate,  db: Session) -> EmployeeOut: 
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

def delete_employee(emp : EmployeeDelete, db: Session):
    db_model = get_employee(emp.cafe_id, emp.id, db)
    db.delete(db_model)
    db.commit()
    return {"message": f"Eintrag mit der id {emp.id} wurde erfolgreich gelöscht"}
