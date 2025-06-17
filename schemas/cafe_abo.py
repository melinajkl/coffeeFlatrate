from pydantic import BaseModel

class AboCafeBase(BaseModel):
    """
    Base schema for the association between a café and an AboModel.

    Attributes:
        cafe_id (str): ID of the associated café.
        abo_id (str): ID of the associated AboModel.
    """
    cafe_id: str
    abo_id: str

class AboCafeCreate(AboCafeBase):
    """
    Schema for creating a new association between a café and an AboModel.
    Inherits all fields from AboCafeBase.
    """
    pass
