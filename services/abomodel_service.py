"""
abomodel_service.py

Service layer for managing AboModels (subscription models). Handles
creation, update, retrieval, and deletion of AboModel entries in the database.
Uses utility CRUD functions for common database operations.
"""

from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import utility_crud
from models.model import AboModel
from schemas.abomodel import AboModelCreate

def create_abomodel(db: Session, model: AboModelCreate) -> AboModel:
    """
    Create a new AboModel (subscription model) entry in the database.

    Args:
        db (Session): The SQLAlchemy session.
        model (AboModelCreate): Data for the new AboModel.

    Returns:
        AboModel: The created AboModel instance.
    """
    db_model = AboModel(
        id=model.id,
        specialdrinks=model.specialdrinks,
        priceperweek=model.priceperweek,
        amount=model.amount
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def patch_abomodel(model: AboModelCreate, db: Session) -> AboModel:
    """
    Update an existing AboModel entry with new data.

    Args:
        model (AboModelCreate): Updated subscription model data.
        db (Session): The SQLAlchemy session.

    Raises:
        HTTPException: If the AboModel with the given ID does not exist.

    Returns:
        AboModel: The updated AboModel instance.
    """
    db_model = db.query(AboModel).filter(AboModel.id == model.id).first()

    if not db_model:
        raise HTTPException(status_code=404, detail="AboModel not found")

    db_model.specialdrinks = model.specialdrinks
    db_model.priceperweek = model.priceperweek
    db_model.amount = model.amount

    db.commit()
    db.refresh(db_model)
    return db_model


def get_all(db: Session) -> List[AboModel]:
    """
    Retrieve all AboModel entries from the database.

    Args:
        db (Session): The SQLAlchemy session.

    Returns:
        List[AboModel]: A list of all AboModel entries.
    """
    return db.query(AboModel).all()


def get_by_id(id: str, db: Session) -> AboModel:
    """
    Retrieve a single AboModel by its unique ID.

    Args:
        id (str): The AboModel ID.
        db (Session): The SQLAlchemy session.

    Returns:
        AboModel: The matching AboModel object.

    Raises:
        HTTPException: If the AboModel does not exist.
    """
    return utility_crud.get_by_id(AboModel, id, db)


def delete_by_id(id: str, db: Session):
    """
    Delete an AboModel from the database by its ID.

    Args:
        id (str): The AboModel ID.
        db (Session): The SQLAlchemy session.

    Returns:
        dict: A confirmation message after deletion.
    """
    return utility_crud.delete_by_id(AboModel, id, db)
