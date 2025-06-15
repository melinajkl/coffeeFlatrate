from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Date, Table, JSON
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import relationship
from uuid import uuid4
from database import Base
import datetime

# Association table for many-to-many between Cafe and AboModel
AboCafe = Table(
    "cafe_abomodel",
    Base.metadata,
    Column("cafe_id", String, ForeignKey("cafes.id"), primary_key=True),
    Column("abo_id", String, ForeignKey("abomodels.id"), primary_key=True)
)

class Cafe(Base):
    __tablename__ = "cafes"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    iban = Column(String)
    bic = Column(String)
    account_holder = Column(String)

    # Corrected many-to-many relationship
    abolist = relationship(
        "AboModel",
        secondary=AboCafe,
        back_populates="cafes"
    )


class AboModel(Base):
    __tablename__ = "abomodels"

    id = Column(String, primary_key=True)
    specialdrinks = Column(Boolean, default=False)
    priceperweek = Column(Integer)
    amount = Column(Integer)

    # Corrected many-to-many relationship
    cafes = relationship(
        "Cafe",
        secondary=AboCafe,
        back_populates="abolist"
    )

class Employee(Base):
    __tablename__ = "employees"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String)
    hashed_password = Column(String)
    sudo = Column(Boolean, default=False)

    cafe_id = Column(String, ForeignKey("cafes.id"))
    cafe = relationship("Cafe", backref="employees")

class Abo(Base):
    __tablename__ = "abos"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    model_id = Column(String, ForeignKey("abomodels.id"))
    customer_id = Column(String, ForeignKey("customers.id"))
    cafe_id = Column(String, ForeignKey("cafes.id"))

    model = relationship("AboModel")
    cafe = relationship("Cafe")

class Customer(Base):
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
