from sqlalchemy.orm import Session
from models.model import AboModel
from models import functions
from schemas.abomodel import AboModelCreate
from fastapi import HTTPException
from typing import List

def create_abomodel(db: Session, model: AboModelCreate) -> AboModel:
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
     # Fetch existing AboModel by id
    db_model = db.query(AboModel).filter(AboModel.id == model.id).first()

    if not db_model:
        raise HTTPException(status_code=404, detail="AboModel not found")

    # Update allowed fields only (not ID)
    db_model.specialdrinks = model.specialdrinks
    db_model.priceperweek = model.priceperweek
    db_model.amount = model.amount

    db.commit()
    db.refresh(db_model)
    return db_model

def get_all(db: Session) -> List[AboModel]:
    return db.query(AboModel).all()
    
def get_by_id(id: str, db: Session) -> AboModel: 
   return functions.get_by_id(AboModel, id, db)

def delete_by_id(id: str, db: Session):
    return functions.delete_by_id(AboModel, id, db)