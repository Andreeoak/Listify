from fastapi import  APIRouter, Depends, status, HTTPException
from Database.database import getDb
from sqlalchemy.orm import Session
from typing import Annotated
from Database.Models.ToDosModel import ToDosModel
from Utils.encryption import jwtEncryption

db_dependency = Annotated[Session, Depends(getDb)]
user_dependency = Annotated[dict, Depends(jwtEncryption.getCurrentUser)]

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)

@router.get("/todo", status_code=status.HTTP_200_OK)
async def getAllTasks(user:user_dependency, db:db_dependency):
    if user is None or user.get('user_role')!= 'admin':
        raise HTTPException(status_code=401, detail="Authentication Failed!")
    return db.query(ToDosModel).all()