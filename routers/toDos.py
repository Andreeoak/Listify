from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
from Database.Models.ToDosModel import ToDosModel
from Database.database import getDb
from Interfaces.TaskInterface import TaskInterface
from Utils.encryption import jwtEncryption

router = APIRouter()
db_dependency = Annotated[Session, Depends(getDb)]
user_dependency = Annotated[dict, Depends(jwtEncryption.getCurrentUser)]

@router.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_to_tasks():
    return RedirectResponse(url="/Tasks")

@router.get("/Tasks", status_code=status.HTTP_200_OK)
async def readAllEntries(user:user_dependency, db: db_dependency):
    todos = db.query(ToDosModel).filter(ToDosModel.owner_id == user["id"]).all()
    return jsonable_encoder(todos, exclude={"owner": {"todos"}}) #lets you skip fields that cause recursion => just exclude the deep nesting in serialization.

@router.get("/Tasks/{task_id}", status_code=status.HTTP_200_OK)
async def readTaskById(db:db_dependency, task_id:int):
    model =db.query(ToDosModel).filter(ToDosModel.id ==task_id).first()
    if(model is not None):
        return model
    raise HTTPException(status_code=404, detail="Task not found")

@router.post("/Tasks", status_code=status.HTTP_201_CREATED)
async def createTask(user:user_dependency, db:db_dependency, task:TaskInterface):
    if(user is None):
        raise HTTPException(status_code=401, detail="Authentication Failed")
    model = ToDosModel(**task.model_dump(), owner_id=user.get("id"))
    db.add(model)
    db.commit()
    db.refresh(model)
    return {"message": "Task created succesfully!", "New Task": task}

@router.put("/Tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def updateTask(db: db_dependency, task_id:int, task:TaskInterface):
    model = db.query(ToDosModel).filter(ToDosModel.id == task_id).first()
    if model is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(model, key, value)
    db.commit()
    
@router.delete("/Tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTask(db: db_dependency, task_id:int):
    model = db.query(ToDosModel).filter(ToDosModel.id == task_id).first()
    if model is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.query(ToDosModel).filter(ToDosModel.id == task_id).delete()
    db.commit()
        