from pydantic import BaseModel

class Token(BaseModel):
    """
    Schema representing an access token response.

    Attributes:
        access_token (str): The generated JWT token used for authentication.
        token_type (str): The type of the token, typically 'bearer'.
    """
    access_token: str
    token_type: str
