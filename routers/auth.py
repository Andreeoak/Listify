from fastapi import  APIRouter, status
from Interfaces.UserInterface import UserInterface
from Database.Models.UsersModel import UsersModel
from Utils.encryption import EncryptionContext

router = APIRouter()

@router.post("/auth/")
async def createUser(createUserRequest: UserInterface):
    create_user_model = UsersModel(
        email = createUserRequest.email,
        username = createUserRequest.username,
        first_name = createUserRequest.first_name,
        last_name= createUserRequest.last_name,
        role = createUserRequest.role,
        hashed_password = EncryptionContext.hashPassword(createUserRequest.password),
        is_active = True
    )
    
    return{ 
        "Message": "User created succesfully!",
        "User":   create_user_model 
    }