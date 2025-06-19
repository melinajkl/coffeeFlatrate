from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, Any

class CustomerCreate(BaseModel):
    """
    Represents the data model for creating a new customer.

    Attributes:
        name (str): Name of the customer.
        password (str): Plain-text password (will be hashed internally).
        email (EmailStr): Unique email address.
        paymentMethod (int): Payment method (0 = Cash, 1 = PayPal).
    """
    name: str
    password: str
    email: EmailStr
    paymentMethod: int


class CustomerOut(BaseModel):
    """
    Schema for safely returning customer data (e.g. after registration or login).

    Attributes:
        id (str): Unique customer ID.
        name (str): Name of the customer.
        email (EmailStr): Email address of the customer.
        drinksDrunk (int): Number of drinks consumed.
        lastPaid (Optional[date]): Date of last payment, if available.
    """
    id: str
    name: str
    email: EmailStr
    drinksDrunk: int
    lastPaid: Optional[date]

    class Config:
        from_attributes = True


class CustomerStats(BaseModel):
    """
    Extended customer information and statistics for internal use or analytics.

    Attributes:
        name (str): Name of the customer.
        email (EmailStr): Email address of the customer.
        drinksDrunk (int): Number of drinks consumed.
        drinkLog (Any): Log of consumed drinks (e.g. list or dictionary).
        activated (bool): Indicates whether the account is active.
    """
    name: str
    email: EmailStr
    drinksDrunk: int 
    drinkLog: Any
    activated: bool
