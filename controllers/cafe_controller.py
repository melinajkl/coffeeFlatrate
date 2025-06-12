from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.cafe import *
from services import cafe_service
from database import get_db

router = APIRouter(prefix="/cafes", tags=["cafe"])

@router.post("/", response_model=CafeCreate)
def create_cafe(model: CafeCreate, db: Session = Depends(get_db)):
    return cafe_service.create_cafe(db, model)