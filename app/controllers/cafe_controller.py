"""
cafe_routes.py

Defines API routes for managing cafés in the system. Includes endpoints
to create, update, retrieve, and delete café records, as well as retrieve
a café with its associated subscription models (AboModels).
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.cafe import CafeCreate, CafeOut, CafeOutB
from services import cafe_service
from app.database import get_db

router = APIRouter(prefix="/cafes", tags=["cafe"])


@router.post("/", response_model=CafeOut)
def create_cafe(model: CafeCreate, db: Session = Depends(get_db)):
    """
    Create a new café in the system.

    Args:
        model (CafeCreate): Data for the new café.
        db (Session): The database session dependency.

    Returns:
        CafeOut: The created café object.
    """
    return cafe_service.create_cafe(db, model)


@router.patch("/", response_model=CafeOut)
def patch_cafe(model: CafeCreate, db: Session = Depends(get_db)):
    """
    Update an existing café's information.

    Args:
        model (CafeCreate): Updated café data.
        db (Session): The database session dependency.

    Returns:
        CafeOut: The updated café object.
    """
    return cafe_service.patch_cafe(model, db)


@router.get("/", response_model=List[CafeOut])
def get_cafes(db: Session = Depends(get_db)):
    """
    Retrieve a list of all cafés in the system.

    Args:
        db (Session): The database session dependency.

    Returns:
        List[CafeOut]: A list of all cafés.
    """
    return cafe_service.get_all_cafes(db)


@router.get("/{id}", response_model=CafeOut)
def cafe_by_id(id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific café by its ID.

    Args:
        id (str): The café's unique ID.
        db (Session): The database session dependency.

    Returns:
        CafeOut: The matching café object.
    """
    return cafe_service.get_by_id(id, db)


@router.delete("/{id}")
def del_cafe(id: str, db: Session = Depends(get_db)):
    """
    Delete a café by its ID.

    Args:
        id (str): The café's unique ID.
        db (Session): The database session dependency.

    Returns:
        dict: A confirmation message upon successful deletion.
    """
    return cafe_service.delete_by_id(id, db)


@router.get("/{id}/abo", response_model=CafeOutB)
def get_cafe_with_abos(id: str, db: Session = Depends(get_db)):
    """
    Retrieve a café including its associated subscription models (AboModels).

    Args:
        id (str): The café's unique ID.
        db (Session): The database session dependency.

    Returns:
        CafeOutB: The café with attached AboModel information.
    """
    return cafe_service.get_cafe_w_abos(id, db)
