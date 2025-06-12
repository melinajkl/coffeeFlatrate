from sqlalchemy.orm import Session
from models.model import Customer
from schemas.customer import CustomerCreate
from utils.security import hash_password
import datetime

def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    db_customer = Customer(
        name=customer.name,
        hashed_password=hash_password(customer.password),
        email=customer.email,
        paymentMethod=customer.paymentMethod,
        lastPaid=datetime.date.today(),
        activated=True
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer
