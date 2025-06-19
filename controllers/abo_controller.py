"""
This module defines routes for managing Abonnements (subscriptions) in the CoffeeClub system.

Endpoints:
- POST /abo/: Create a new Abo (subscription) for a user.

All endpoints require a valid access token and interact with the Abo service layer.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.abo import AboCreate
from schemas.token import Token
from services import abo_service
from database import get_db
from utils.security import verify_access_token

router = APIRouter(
    prefix="/abo",
    tags=["abo"]
)

@router.post("/", summary="Create a new subscription (Abo)")
def create_new_abonnement(
    abo: AboCreate,
    db: Session = Depends(get_db),
    token_data: Token = Depends(verify_access_token)  # auto-extracts and validates token
):
    """
    Creates a new Abo (subscription) for the authenticated user.

    Args:
        abo (AboCreate): The Abo creation payload containing model_id, start date, etc.
        db (Session): SQLAlchemy session for database operations.
        token_data (Token): Decoded token data containing the user's identity and roles.

    Returns:
        dict: A dictionary representing the newly created Abo.

    Raises:
        HTTPException: If the user is unauthorized or the Abo cannot be created.

    This endpoint allows a non-admin user to register an Abo for a customer.
    Only valid users with a token can access this route.
    """
    return abo_service.create_abo(abo, db, token_data)
