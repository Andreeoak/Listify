from fastapi import  APIRouter, Depends, status
from Interfaces.UserInterface import UserInterface
from Database.Models.UsersModel import UsersModel
from Utils.encryption import EncryptionContext
from Database.database import getDb
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter()
db_dependency = Annotated[Session, Depends(getDb)]

@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def createUser(db:db_dependency, createUserRequest: UserInterface):
    create_user_model = UsersModel(
        email = createUserRequest.email,
        username = createUserRequest.username,
        first_name = createUserRequest.first_name,
        last_name= createUserRequest.last_name,
        role = createUserRequest.role,
        hashed_password = EncryptionContext.hashPassword(createUserRequest.password),
        is_active = True
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return{ 
        "Message": "User created succesfully!",
        "User":   create_user_model 
    }