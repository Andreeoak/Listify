from fastapi import  APIRouter, Depends, status
from Interfaces.UserInterface import UserInterface
from Database.Models.UsersModel import UsersModel
from Utils.encryption import EncryptionContext
from Database.database import getDb
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
db_dependency = Annotated[Session, Depends(getDb)]

def authenticate_user(username:str, password:str, db:db_dependency):
    user = db.query(UsersModel).filter(UsersModel.username==username).first()
    if(not user):
        return False
    if(not EncryptionContext.verifyPassword(password, user.hashed_password)):
        return False
    return True


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
    
@router.post("/token")
async def loginForAccessToken(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if(not user):
        return "Failed Authentication"
    return "Authentication Successful!"