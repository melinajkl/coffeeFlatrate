# routers/abo_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.abo import AboCreate
from schemas.token import Token
from services import abo_service
from database import get_db
from utils.security import verify_access_token

router = APIRouter(prefix="/abo", tags=["abo"])

@router.post("/")
def create_new_abonnement(
    abo: AboCreate,
    db: Session = Depends(get_db),
    token_data: Token = Depends(verify_access_token)  # auto-extracts and validates token
):
    return abo_service.create_abo(abo, db, token_data)
