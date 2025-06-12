from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.abomodel import AboModelCreate, AboModelBase
from services import abomodel_service
from database import get_db
from typing import List

router = APIRouter(prefix="/abomodels", tags=["abo models"])

@router.post("/", response_model=AboModelBase)
def create_abomodel(model: AboModelCreate, db: Session = Depends(get_db)):
    return abomodel_service.create_abomodel(db, model)

@router.patch("/", response_model=AboModelBase)
def adjust_abomodel(model: AboModelCreate, db: Session = Depends(get_db)):
    return abomodel_service.patch_abomodel(model, db)

@router.get("/", response_model=List[AboModelBase])
def get_all_abomodels(db: Session = Depends(get_db)):
    return abomodel_service.get_all(db)

@router.get("/{id}", response_model = AboModelBase)
def get_by_id(id: str, db: Session = Depends(get_db)):
    return abomodel_service.get_by_id(id, db)

@router.delete("/{id}")
def delete_model(id: str, db:Session = Depends(get_db)):
    return abomodel_service.delete_by_id(id, db)