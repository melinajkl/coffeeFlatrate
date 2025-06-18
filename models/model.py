"""
models.py

This module defines the SQLAlchemy ORM models for a café subscription system.
It includes models for Cafés, AboModels (subscription types), Employees, Customers,
Abos (individual subscriptions), and the many-to-many relationship between Cafés and AboModels.
"""
from uuid import uuid4
from sqlalchemy import Column, PrimaryKeyConstraint, String, Boolean
from sqlalchemy import Integer, ForeignKey, Date, Table, JSON
from sqlalchemy.orm import relationship
from database import Base

# Association table for many-to-many between Cafe and AboModel
AboCafe = Table(
    "cafe_abomodel",
    Base.metadata,
    Column("cafe_id", String, ForeignKey("cafes.id"), primary_key=True),
    Column("abo_id", String, ForeignKey("abomodels.id"), primary_key=True)
)

class Cafe(Base):
    """
    Represents a Café entity which offers subscription models (AboModels).
    
    Attributes:
        id (str): UUID identifier for the café.
        iban (str): IBAN for payments.
        bic (str): BIC for bank identification.
        account_holder (str): Name of the account owner.
        abolist (List[AboModel]): Subscriptions offered by the café.
        employees (List[Employee]): Employees working in this café.
    """
    __tablename__ = "cafes"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    iban = Column(String)
    bic = Column(String)
    account_holder = Column(String)

    abolist = relationship(
        "AboModel",
        secondary=AboCafe,
        back_populates="cafes"
    )
    employees = relationship("Employee", back_populates="cafe")


class AboModel(Base):
    """
    Represents a subscription model offered by cafés.

    Attributes:
        id (str): Unique identifier for the model.
        specialdrinks (bool): Whether special drinks are included.
        priceperweek (int): Cost per week for the subscription.
        amount (int): Number of drinks per week.
        cafes (List[Cafe]): Cafés offering this model.
    """
    __tablename__ = "abomodels"

    id = Column(String, primary_key=True)
    specialdrinks = Column(Boolean, default=False)
    priceperweek = Column(Integer)
    amount = Column(Integer)

    cafes = relationship(
        "Cafe",
        secondary=AboCafe,
        back_populates="abolist"
    )


class Employee(Base):
    """
    Represents an employee working at a café.

    Composite Primary Key:
        id + cafe_id

    Attributes:
        id (str): Employee ID (unique within a café).
        cafe_id (str): ID of the café the employee belongs to.
        name (str): Full name of the employee.
        hashed_password (str): Secured password hash.
        sudo (bool): Admin privileges flag.
        cafe (Cafe): Associated café.
    """
    __tablename__ = "employees"

    id = Column(String, nullable=False)
    cafe_id = Column(String, ForeignKey("cafes.id"), nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    sudo = Column(Boolean, default=False)

    __table_args__ = (
        PrimaryKeyConstraint('id', 'cafe_id'),
    )

    cafe = relationship("Cafe", back_populates="employees")


class Abo(Base):
    """
    Represents an active subscription (instance of an AboModel) for a customer.

    Attributes:
        id (str): UUID of the Abo.
        model_id (str): Foreign key to AboModel.
        customer_id (str): Foreign key to Customer.
        cafe_id (str): Foreign key to Café where the Abo is used.
        model (AboModel): Subscription model used.
        cafe (Cafe): Café associated with the subscription.
    """
    __tablename__ = "abos"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    model_id = Column(String, ForeignKey("abomodels.id"))
    customer_id = Column(String, ForeignKey("customers.id"))
    cafe_id = Column(String, ForeignKey("cafes.id"))

    model = relationship("AboModel")
    cafe = relationship("Cafe")


class Customer(Base):
    """
    Represents a customer who can subscribe to up to two subscription models.

    Attributes:
        id (str): UUID for the customer.
        name (str): Full name.
        hashed_password (str): Secured password hash.
        lastPaid (Date): Last successful payment date.
        activated (bool): Whether the customer account is active.
        paymentMethod (int): 0 for Cash, 1 for PayPal.
        email (str): Unique email address.
        drinksDrunk (int): Total number of drinks consumed.
        drinkLog (JSON): Detailed log of drink history.
        abo1_id (str): First active subscription ID.
        abo2_id (str): Second active subscription ID.
        abo1 (Abo): First subscription relation.
        abo2 (Abo): Second subscription relation.
    """
    __tablename__ = "customers"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String)
    hashed_password = Column(String)
    lastPaid = Column(Date)
    activated = Column(Boolean, default=True)
    paymentMethod = Column(Integer)  # 0 = Cash, 1 = PayPal
    email = Column(String, unique=True)
    drinksDrunk = Column(Integer, default=0)
    drinkLog = Column(JSON, default=[])

    abo1_id = Column(String, ForeignKey("abos.id"))
    abo2_id = Column(String, ForeignKey("abos.id"))

    abo1 = relationship("Abo", foreign_keys=[abo1_id])
    abo2 = relationship("Abo", foreign_keys=[abo2_id])
