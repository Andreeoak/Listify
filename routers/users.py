from fastapi import  APIRouter, Depends, status, HTTPException, Path
from Database.database import getDb
from sqlalchemy.orm import Session
from typing import Annotated
from Database.Models.UsersModel import UsersModel
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

