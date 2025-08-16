from fastapi import  APIRouter, Depends, status, HTTPException, Path
from Database.database import getDb
from sqlalchemy.orm import Session
from typing import Annotated
from Database.Models.UsersModel import UsersModel
from Interfaces.UserVerificationInterface import UserVerificationInterface as UserVerification
from Utils.encryption import jwtEncryption
from Utils.encryption import EncryptionContext

db_dependency = Annotated[Session, Depends(getDb)]
user_dependency = Annotated[dict, Depends(jwtEncryption.getCurrentUser)]
bcrypt_context = EncryptionContext._bcrypt_context

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.get("/", status_code=status.HTTP_200_OK)
async def getUser(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed!')
    return db.query(UsersModel).filter(UsersModel.id == user.get("id")).first()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def changeUserPassword(user:user_dependency, db:db_dependency, user_verification:UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed!')
    user_model = db.query(UsersModel).filter(UsersModel.id == user.get('id')).first()
    
    if not EncryptionContext.verifyPassword(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Could not confirm password.')
    user_model.hashed_password = EncryptionContext.hashPassword(user_verification.new_password)
    db.add(user_model)
    db.commit()