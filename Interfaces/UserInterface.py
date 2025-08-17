from pydantic import BaseModel

class UserInterface(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str
    phone_number:str