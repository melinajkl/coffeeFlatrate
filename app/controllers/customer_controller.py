"""
customer_router.py

This module defines the API endpoints for customer registration, login, 
profile update, overview, and statistics using FastAPI.

Endpoints:
- POST /customers/: Register a new customer.
- POST /customers/login: Log in a customer and return a JWT token.
- PATCH /customers/{id}: Update customer profile.
- GET /customers/{id}/overview: Get customer profile overview.
- GET /customers/{id}/details: Get customer usage statistics.
"""
from pydantic import EmailStr
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from schemas.customer import CustomerCreate, CustomerOut
from schemas.token import Token
from services import customer_service, auth_service
from app.database import get_db

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=CustomerOut)
def register_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """
    Register a new customer account.

    Args:
        customer (CustomerCreate): Customer data from the request body.
        db (Session): SQLAlchemy database session dependency.

    Returns:
        CustomerOut: The created customer object.
    """
    return customer_service.create_customer(db, customer)


@router.post("/login", response_model=Token)
def login_customer(email: EmailStr = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """
    Authenticates a customer and returns a JWT access token.

    Args:
        email (EmailStr): Customer's email from form data.
        password (str): Customer's password from form data.
        db (Session): SQLAlchemy database session dependency.

    Returns:
        Token: Access token and token type.
    """
    token = auth_service.authenticate_customer(db, email, password)
    return {"access_token": token, "token_type": "bearer"}


@router.patch("/{id}", response_model=CustomerOut)
def patch_customer(id: str, customer: CustomerCreate, db: Session = Depends(get_db)):
    """
    Update customer information.

    Args:
        id (str): Customer's unique identifier.
        customer (CustomerCreate): Updated customer data.
        db (Session): SQLAlchemy database session dependency.

    Returns:
        CustomerOut: The updated customer object.
    """
    return customer_service.patch_customer(id, customer, db)


@router.get("/{id}/overview", response_model=CustomerOut)
def overview_customer(id: str, db: Session = Depends(get_db)):
    """
    Retrieves an overview of the customer's profile.

    Args:
        id (str): Customer's unique identifier.
        db (Session): SQLAlchemy database session dependency.

    Returns:
        CustomerOut: Customer profile overview.
    """
    return customer_service.overview(id, db)


@router.get("/{id}/details")
def get_stats(id: str, db: Session = Depends(get_db)):
    """
    Returns usage statistics for a specific customer.

    Args:
        id (str): Customer's unique identifier.
        db (Session): SQLAlchemy database session dependency.

    Returns:
        dict: Statistical data about the customer's activity.
    """
    return customer_service.statistics(id, db)
