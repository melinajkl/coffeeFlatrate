from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.customer import CustomerCreate, CustomerOut
from services import customer_service
from database import get_db

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=CustomerOut)
def register_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return customer_service.create_customer(db, customer)
