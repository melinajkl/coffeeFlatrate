from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.cafe import *
from services import cafe_service
from database import get_db

router = APIRouter(prefix="/cafes", tags=["cafe"])

@router.post("/", response_model=CafeOut)
def create_cafe(model: CafeCreate, db: Session = Depends(get_db)):
    return cafe_service.create_cafe(db, model)

@router.patch("/", response_model=CafeOut)
def patch_cafe(model: CafeCreate, db:Session = Depends(get_db)):
    return cafe_service.patch_cafe(model, db)

@router.get("/", response_model=List[CafeOut])
def get_cafes(db: Session = Depends(get_db)):
    return cafe_service.get_all_cafes(db)

@router.get("/{id}", response_model=CafeOut)
def cafe_by_id(id: str, db:Session = Depends(get_db)):
    return cafe_service.get_by_id(id, db)

@router.delete("/{id}")
def del_cafe(id:str, db: Session = Depends(get_db)):
    return cafe_service.delete_by_id(id, db)

@router.get("/{id}/abo", response_model=CafeOutB)
def get_cafe_with_abos(id: str, db: Session = Depends(get_db)):
    return cafe_service.get_cafe_w_abos(id, db)