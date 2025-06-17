"""
abomodel_routes.py

This module defines API routes for managing AboModel entities (subscription models)
in the system. It includes endpoints for creating, updating, retrieving, and deleting
subscription models used by cafés.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.abomodel import AboModelCreate, AboModelBase
from services import abomodel_service
from app.database import get_db

router = APIRouter(prefix="/abomodels", tags=["abo models"])


@router.post("/", response_model=AboModelBase)
def create_abomodel(model: AboModelCreate, db: Session = Depends(get_db)):
    """
    Create a new AboModel (subscription model).

    Args:
        model (AboModelCreate): The subscription model data.
        db (Session): The database session dependency.

    Returns:
        AboModelBase: The newly created subscription model.
    """
    return abomodel_service.create_abomodel(db, model)


@router.patch("/", response_model=AboModelBase)
def adjust_abomodel(model: AboModelCreate, db: Session = Depends(get_db)):
    """
    Update an existing AboModel based on its ID.

    Args:
        model (AboModelCreate): Updated subscription model data.
        db (Session): The database session dependency.

    Returns:
        AboModelBase: The updated subscription model.
    """
    return abomodel_service.patch_abomodel(model, db)


@router.get("/", response_model=List[AboModelBase])
def get_all_abomodels(db: Session = Depends(get_db)):
    """
    Retrieve all AboModels from the database.

    Args:
        db (Session): The database session dependency.

    Returns:
        List[AboModelBase]: A list of all available subscription models.
    """
    return abomodel_service.get_all(db)


@router.get("/{id}", response_model=AboModelBase)
def get_by_id(id: str, db: Session = Depends(get_db)):
    """
    Retrieve a single AboModel by its ID.

    Args:
        id (str): The ID of the subscription model.
        db (Session): The database session dependency.

    Returns:
        AboModelBase: The matching subscription model.
    """
    return abomodel_service.get_by_id(id, db)


@router.delete("/{id}")
def delete_model(id: str, db: Session = Depends(get_db)):
    """
    Delete an AboModel by its ID.

    Args:
        id (str): The ID of the subscription model to delete.
        db (Session): The database session dependency.

    Returns:
        dict: A confirmation message after deletion.
    """
    return abomodel_service.delete_by_id(id, db)
