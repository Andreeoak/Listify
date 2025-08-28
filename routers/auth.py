from fastapi import  APIRouter, Depends, status, HTTPException, Request
from fastapi.templating import Jinja2Templates
from Interfaces.UserInterface import UserInterface
from Interfaces.TokenInterface import TokenInterface
from Database.Models.UsersModel import UsersModel
from Utils.encryption import EncryptionContext, jwtEncryption
from Database.database import getDb
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)
db_dependency = Annotated[Session, Depends(getDb)]

templates = Jinja2Templates(directory="Templates")
### Page Mounting ###

@router.get("/login-page")
def render_login_page(request:Request):
    return templates.TemplateResponse("login.html", { "request": request})

@router.get("/register-page")
def render_register_page(request:Request):
    return templates.TemplateResponse("register.html", { "request": request})

### Endpoints ###

def authenticate_user(username:str, password:str, db:db_dependency):
    user = db.query(UsersModel).filter(UsersModel.username==username).first()
    if(not user):
        return False
    if(not EncryptionContext.verifyPassword(password, user.hashed_password)):
        return False
    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
async def createUser(db: db_dependency, createUserRequest: UserInterface):
    try:
        create_user_model = UsersModel(
            email=createUserRequest.email,
            username=createUserRequest.username,
            first_name=createUserRequest.first_name,
            last_name=createUserRequest.last_name,
            role=createUserRequest.role,
            phone_number=createUserRequest.phone_number,
            hashed_password=EncryptionContext.hashPassword(createUserRequest.password),
            is_active=True
        )
        db.add(create_user_model)
        db.commit()
        db.refresh(create_user_model)

        return {"message": "User created successfully!"}

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email or username already exists."
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    
@router.post("/token", response_model=TokenInterface)
async def loginForAccessToken(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if(not user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify credentials")
    token = jwtEncryption.createAccessToken(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token':token, "token_type": 'bearer'}