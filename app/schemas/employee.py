from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    """
    Schema for creating a new employee.

    Attributes:
        id (str): Unique employee ID (e.g., personnel number).
        name (str): Name of the employee.
        password (str): Plain-text password (to be hashed server-side).
        sudo (bool): Indicates whether the employee has admin privileges.
        cafe_id (str): Reference to the café where the employee works.
    """
    id: str
    name: str
    password: str
    sudo: bool = False
    cafe_id: str


class EmployeeOut(BaseModel):
    """
    Output schema for employee data (e.g., for lists or profiles).

    Attributes:
        id (str): Employee ID.
        name (str): Name of the employee.
        sudo (bool): Indicates whether the employee has admin privileges.
    """
    id: str
    name: str
    sudo: bool

    class Config:
        orm_mode = True


class EmployeeDelete(BaseModel):
    """
    Schema used to identify an employee when deleting.

    Attributes:
        id (str): Employee ID.
        cafe_id (str): Associated café ID for composite key matching.
    """
    id: str
    cafe_id: str
