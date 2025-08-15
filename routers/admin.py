from fastapi import  APIRouter, Depends, status, HTTPException, Path
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


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def getAllTasks(user:user_dependency, db:db_dependency, todo_id:int = Path(gt=0)):
    if user is None or user.get('user_role')!= 'admin':
        raise HTTPException(status_code=401, detail="Authentication Failed!")
    model = db.query(ToDosModel).filter(ToDosModel.id == todo_id).first()
    if(model is None):
        raise HTTPException(status_code=404, detail=f"No records found with id= {todo_id}")
    db.query(ToDosModel).filter(ToDosModel.id == todo_id).delete()
    db.commit()