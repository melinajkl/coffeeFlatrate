"""
utility_crud.py

This module provides generic CRUD utility functions for SQLAlchemy models.
It allows you to retrieve and delete records from any table using their ID.
"""

from typing import Type
from sqlalchemy.orm import Session
from fastapi import HTTPException
from database import Base  # Import your declarative base class


def get_by_id(table: Type[Base], id: str, db: Session):
    """
    Retrieve a single database entry by its ID.

    Args:
        table (Type[Base]): The SQLAlchemy model class (table).
        id (str): The primary key of the record to retrieve.
        db (Session): The active SQLAlchemy session.

    Returns:
        Base: The model instance if found.

    Raises:
        HTTPException: If no entry with the given ID is found.
    """
    model = db.query(table).filter(table.id == id).first()

    if not model:
        raise HTTPException(status_code=404, detail="No model with given id found.")
    
    return model


def delete_by_id(table: Type[Base], id: str, db: Session):
    """
    Delete a database entry by its ID.

    Args:
        table (Type[Base]): The SQLAlchemy model class (table).
        id (str): The primary key of the record to delete.
        db (Session): The active SQLAlchemy session.

    Returns:
        dict: A confirmation message after deletion.

    Raises:
        HTTPException: If no entry with the given ID is found.
    """
    model = get_by_id(table, id, db)
    db.delete(model)
    db.commit()
    return {
        "message": f"{table.__tablename__}-Eintrag mit der id {id} wurde erfolgreich gelöscht"
    }
