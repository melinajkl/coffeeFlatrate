# services/abo_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.token import Token
from schemas.abo import AboCreate
from models.model import Abo, AboModel, Cafe

def create_abo(abo: AboCreate, db: Session, token_data: Token):
    # Optional: enforce access control, e.g. same cafe
    if token_data.cafe_id != abo.cafe_id:
        raise HTTPException(status_code=403, detail="You can only create Abos for your own café")

    # Check if the café exists
    cafe = db.query(Cafe).filter(Cafe.id == abo.cafe_id).first()
    if not cafe:
        raise HTTPException(status_code=404, detail="Café not found.")

    # Check if the café offers the Abo model
    abomodel = db.query(AboModel).filter(
        AboModel.id == abo.model_id,
        AboModel.cafe_id == abo.cafe_id
    ).first()

    if not abomodel:
        raise HTTPException(status_code=400, detail="This café does not offer the selected Abo model.")

    # Prevent multiple Abos per customer
    existing_abo = db.query(Abo).filter(Abo.customer_id == abo.customer_id).first()
    if existing_abo:
        raise HTTPException(status_code=409, detail="Customer already has an active Abo.")

    # Create and persist new Abo
    new_abo = Abo(
        model_id=abo.model_id,
        cafe_id=abo.cafe_id,
        customer_id=abo.customer_id
    )

    db.add(new_abo)
    db.commit()
    db.refresh(new_abo)
    return new_abo