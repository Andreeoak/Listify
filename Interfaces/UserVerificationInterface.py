from pydantic import BaseModel, Field

class UserVerificationInterface(BaseModel):
    password: str
    new_password: str = Field(min_length=6)