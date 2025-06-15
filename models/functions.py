from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Type
from database import Base  # oder dein Base-Modul mit declarative_base()


def get_by_id(table: Type[Base], id: str, db: Session):
    model = db.query(table).filter(table.id == id).first()
    
    if not model:
        raise HTTPException(status_code=404, detail="No model with given id found.")
    
    return model

def delete_by_id(table: Type[Base], id: str, db: Session):
    model = get_by_id(table, id, db)
    db.delete(model)
    db.commit()
    return {"message": f"{table.__tablename__}-Eintrag mit der id {id} wurde erfolgreich gelöscht"}
