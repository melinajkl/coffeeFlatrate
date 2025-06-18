"""
customer_service.py

Provides business logic for managing customers in the backend system.

Includes functionality to:
- Create a new customer
- Retrieve a customer profile
- Update customer details
- Fetch customer consumption statistics
"""
import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.model import Customer
from models.utility_crud import get_by_id
from schemas.customer import CustomerCreate, CustomerOut, CustomerStats
from utils.security import hash_password

def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    """
    Create a new customer account and store it in the database.

    Args:
        db (Session): SQLAlchemy session for database interaction.
        customer (CustomerCreate): Pydantic schema with customer registration details.

    Returns:
        Customer: The newly created Customer database object.
    """
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


def overview(ida: str, db: Session) -> CustomerOut:
    """
    Retrieve a customer's profile by ID.

    Args:
        id (str): The customer's unique identifier.
        db (Session): SQLAlchemy database session.

    Returns:
        CustomerOut: Public-facing customer profile data.
    """
    return get_by_id(Customer, ida, db)


def patch_customer(ida: str, customer: CustomerCreate, db: Session) -> CustomerOut:
    """
    Update a customer's account information.

    Args:
        id (str): Unique ID of the customer to update.
        customer (CustomerCreate): Schema containing updated customer fields.
        db (Session): SQLAlchemy session.

    Returns:
        CustomerOut: Updated customer profile.

    Raises:
        HTTPException: If customer ID is invalid.
    """
    db_customer = get_by_id(Customer, ida, db)

    if not db_customer:
        raise HTTPException(status_code=401, detail="Invalid user id")

    db_customer.name = customer.name
    db_customer.hashed_password = hash_password(customer.password)
    db_customer.email = customer.email
    db_customer.paymentMethod = customer.paymentMethod

    db.commit()
    db.refresh(db_customer)
    return overview(db_customer.id, db)


def statistics(ida: str, db: Session) -> CustomerStats:
    """
    Retrieve customer-specific consumption and status statistics.

    Args:
        id (str): The customer's ID.
        db (Session): SQLAlchemy session.

    Returns:
        CustomerStats: Structured data about customer's drink activity and status.
    """
    customer = get_by_id(Customer, ida, db)
    out = CustomerStats(
        name=customer.name,
        email=customer.email,
        drinksDrunk=customer.drinksDrunk,
        drinkLog=customer.drinkLog,
        activated=customer.activated
    )
    return out
