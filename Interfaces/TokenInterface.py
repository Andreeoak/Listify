from pydantic import BaseModel


class TokenInterface(BaseModel):
    access_token:str
    token_type: str