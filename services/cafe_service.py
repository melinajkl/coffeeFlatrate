from sqlalchemy.orm import Session
from models.model import Cafe, AboModel
from models import functions
from schemas.cafe import CafeCreate, CafeOut, CafeOutB
from fastapi import HTTPException
from utils import validation

def create_cafe(db: Session, cafe_data: CafeCreate) -> Cafe:
    # Neues Cafe-Objekt (ID wird automatisch generiert)
    cafe = Cafe(
        id = cafe_data.id.replace(" ", "_"),
        iban=cafe_data.iban,
        bic=cafe_data.bic,
        account_holder=cafe_data.account_holder
    )

    # AboModel-IDs aus dem Request hinzufügen
    for abo_id in cafe_data.abomodels:
        abo = db.query(AboModel).filter(AboModel.id == abo_id).first()
        if abo:
            cafe.abolist.append(abo)  # Many-to-Many-Verknüpfung automatisch via ORM

    db.add(cafe)
    db.commit()
    db.refresh(cafe)
    return cafe

def get_all_cafes(db: Session):
    return db.query(Cafe).all()

def get_by_id(id: str, db: Session):
    return functions.get_by_id(Cafe, id, db)

def delete_by_id(id: str, db:Session):
    return functions.delete_by_id(Cafe, id, db)

def get_cafe_w_abos(cafe_id: str, db: Session) -> CafeOutB:
    cafe = db.query(Cafe).filter(Cafe.id == cafe_id).first()
    if not cafe:
        raise HTTPException(status_code=404, detail="Café not found")
    
    return CafeOutB(
        id=cafe.id,
        iban=cafe.iban,
        bic=cafe.bic,
        account_holder=cafe.account_holder,
        abomodels=[abo.id for abo in cafe.abolist]
    )

def patch_cafe(model: CafeCreate, db: Session) -> CafeOut:
    validation.validate_bankdetails(model.iban, model.bic)
    db_model = get_by_id(model.id, db)
    
    # Update allowed fields only (not ID)
   
    db_model.iban = model.iban
    db_model.bic = model.bic
    db_model.account_holder = model.account_holder
    for abo_id in model.abomodels:
        abo = db.query(AboModel).filter(AboModel.id == abo_id).first()
        if abo and abo not in db_model.abolist:
            db_model.abolist.append(abo) # Many-to-Many-Verknüpfung automatisch via ORM
    db.commit()
    db.refresh(db_model)
    return get_cafe_w_abos(model.id, db)