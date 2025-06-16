from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from schemas.customer import CustomerCreate, CustomerOut
from schemas.token import Token
from services import customer_service, auth_service
from database import get_db
from pydantic import EmailStr

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=CustomerOut)
def register_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return customer_service.create_customer(db, customer)

@router.post("/login", response_model=Token)
def login_customer(email: EmailStr = Form(...), password: str = Form(...), db: Session = Depends()):
    token = auth_service.authenticate_customer(db, email, password)
    return {"access toke": token, "token_type": "bearer"}

@router.patch("/{id}", response_model= CustomerOut)
def patch_customer(id:str, customer: CustomerCreate, db: Session = Depends(get_db)):
    return customer_service.patch_customer(id, customer, db) #<<<

@router.get("/{id}/overview", response_model= CustomerOut)
def overview_customer(id: str, db: Session = Depends(get_db)):
    return customer_service.overview(id, db) #<<<

@router.get("/{id}/details")
def get_stats(id: str, db: Session = Depends(get_db)):
    return customer_service.statistics(id, db)