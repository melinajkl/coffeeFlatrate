from sqlalchemy.orm import Session
from models.model import Employee
from schemas.employee import EmployeeCreate
from utils.security import hash_password

def create_employee(db: Session, data: EmployeeCreate) -> Employee:
    db_employee = Employee(
        name=data.name,
        hashed_password=hash_password(data.password),
        sudo=data.sudo,
        cafe_id=data.cafe_id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee