from sqlalchemy.orm import Session
from models.model import Cafe, AboModel
from schemas.cafe import CafeCreate
 
def create_cafe(db: Session, cafe_data: CafeCreate) -> Cafe:
    abomodels = db.query(AboModel).filter(AboModel.id.in_(cafe_data.abolist)).all()

    cafe = Cafe(
        id=cafe_data.id,
        iban=cafe_data.iban,
        bic=cafe_data.bic,
        account_holder=cafe_data.account_holder
    )
    db.add(cafe)
    db.commit()
    db.refresh(cafe)
    return cafe