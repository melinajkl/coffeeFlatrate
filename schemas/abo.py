from pydantic import BaseModel

class AboCreate(BaseModel):
    """
    Schema for creating a new Abo (subscription) entry.

    Attributes:
        model_id (str): ID of the associated AboModel.
        cafe_id (str): ID of the café where the subscription is valid.
    """
    model_id: str
    cafe_id: str
