from sqlalchemy.orm import Session
from models.model import Customer
from utility_crud import *
from schemas.customer import CustomerCreate, CustomerOut, CustomerStats
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

def overview(id: str, db: Session) -> CustomerOut:
    return get_by_id(Customer, id, db)

def patch_customer(id: str, customer: CustomerCreate, db: Session) -> CustomerOut:
    db_customer = get_by_id(Customer, id, db)
    
    if not db_customer:
        raise HTTPException(status_code=401, detail="Invalid user id")
    
    db_customer.name = customer.name
    db_customer.hashed_password = hash_password(customer.password)
    db_customer.email = customer.email
    db_customer.paymentMethod = customer.paymentMethod
    
    db.commit()
    db.refresh(db_customer)
    return overview(db_customer.id, db)

def statistics(id: str, db: Session) -> CustomerStats:
    customer = get_by_id(Customer, id, db)
    out = CustomerStats(
        name= customer.name,
        email=customer.email, 
        drinksDrunk=customer.drinksDrunk,
        drinkLog=customer.drinkLog,
        activated=customer.activated)
    return out