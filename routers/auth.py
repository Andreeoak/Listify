from fastapi import  APIRouter, status
from Interfaces.UserInterface import UserInterface
from Database.Models.UsersModel import UsersModel

router = APIRouter()

@router.post("/auth/", status_code=status.HTTP_204_NO_CONTENT)
async def createUser(createUserRequest: UserInterface):
    create_user_model = UsersModel(
        email = createUserRequest.email,
        username = createUserRequest.username,
        first_name = createUserRequest.first_name,
        last_name= createUserRequest.last_name,
        role = createUserRequest.role,
        hashed_password = createUserRequest.password,
        is_active = True
    )
    
    return{ 
        "Message": "User created succesfully!",
        "User":   create_user_model 
    }