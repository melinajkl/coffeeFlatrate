from pydantic import BaseModel

class AboModelBase(BaseModel):
    """
    Base schema for AboModel with all relevant attributes.

    Attributes:
        id (str): Unique ID of the subscription model.
        specialdrinks (bool): Indicates whether the subscription includes special drinks.
        priceperweek (int): Weekly price in the selected currency unit.
        amount (int): Number of included drinks or units.
    """
    id: str
    specialdrinks: bool
    priceperweek: int
    amount: int

    class Config:
        from_attributes = True 


class AboModelCreate(AboModelBase):
    """
    Schema for creating a new AboModel.
    Inherits all attributes from AboModelBase without modification.
    """
