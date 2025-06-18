"""
cafe_service.py

This module provides business logic for managing cafés in the backend system.
It includes operations for creating, updating, retrieving, and deleting cafés,
as well as associating cafés with subscription models (AboModels).

Functions:
    - create_cafe: Create a new café with optional AboModel associations.
    - get_all_cafes: Retrieve a list of all cafés.
    - get_by_id: Retrieve a café by its ID.
    - delete_by_id: Delete a café by its ID.
    - get_cafe_w_abos: Retrieve a café and its associated AboModels.
    - patch_cafe: Update café details and link new AboModels.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.model import Cafe, AboModel
from models import utility_crud
from schemas.cafe import CafeCreate, CafeOut, CafeOutB
from utils import validation


def create_cafe(db: Session, cafe_data: CafeCreate) -> Cafe:
    """
    Create a new Café and associate it with one or more AboModels.

    Args:
        db (Session): SQLAlchemy session to interact with the database.
        cafe_data (CafeCreate): Input schema containing café and AboModel details.

    Returns:
        Cafe: The created Café instance with relationships persisted.
    """
    cafe = Cafe(
        id=cafe_data.id.replace(" ", "_"),
        iban=cafe_data.iban,
        bic=cafe_data.bic,
        account_holder=cafe_data.account_holder
    )

    for abo_id in cafe_data.abomodels:
        abo = db.query(AboModel).filter(AboModel.id == abo_id).first()
        if abo:
            cafe.abolist.append(abo)  # Many-to-Many linking

    db.add(cafe)
    db.commit()
    db.refresh(cafe)
    return cafe


def get_all_cafes(db: Session):
    """
    Fetch all cafés from the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        List[Cafe]: A list of all cafés.
    """
    return db.query(Cafe).all()


def get_by_id(ida: str, db: Session):
    """
    Retrieve a café by its ID.

    Args:
        id (str): The unique café ID.
        db (Session): SQLAlchemy database session.

    Returns:
        Cafe: The Café instance if found, otherwise None.
    """
    return utility_crud.get_by_id(Cafe, ida, db)


def delete_by_id(ida: str, db: Session):
    """
    Delete a café by its ID.

    Args:
        id (str): The unique café ID.
        db (Session): SQLAlchemy database session.

    Returns:
        bool: True if deleted, False otherwise.
    """
    return utility_crud.delete_by_id(Cafe, ida, db)


def get_cafe_w_abos(cafe_id: str, db: Session) -> CafeOutB:
    """
    Retrieve a café by ID, including all associated AboModel IDs.

    Args:
        cafe_id (str): Unique ID of the café.
        db (Session): SQLAlchemy database session.

    Returns:
        CafeOutB: A café representation including linked AboModels.

    Raises:
        HTTPException: If café with given ID is not found.
    """
    cafe = db.query(Cafe).filter(Cafe.id == cafe_id).first()
    if not cafe:
        raise HTTPException(status_code=404, detail="Café not found")
    
    return CafeOutB(
        id=cafe.id,
        iban=cafe.iban,
        bic=cafe.bic,
        account_holder=cafe.account_holder,
        abomodels=[abo.id for abo in cafe.abolist]
    )


def patch_cafe(model: CafeCreate, db: Session) -> CafeOut:
    """
    Update an existing café's bank details and optionally add new AboModel links.

    Args:
        model (CafeCreate): Input schema with updated café details.
        db (Session): SQLAlchemy session for DB access.

    Returns:
        CafeOut: Updated café details with associated AboModels.

    Raises:
        HTTPException: If validation or update fails.
    """
    validation.validate_bankdetails(model.iban, model.bic)
    db_model = get_by_id(model.id, db)
    
    db_model.iban = model.iban
    db_model.bic = model.bic
    db_model.account_holder = model.account_holder

    for abo_id in model.abomodels:
        abo = db.query(AboModel).filter(AboModel.id == abo_id).first()
        if abo and abo not in db_model.abolist:
            db_model.abolist.append(abo)

    db.commit()
    db.refresh(db_model)
    return get_cafe_w_abos(model.id, db)
