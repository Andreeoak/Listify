from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
from Database.Models.ToDosModel import ToDosModel
from Database.database import engine, Base, getDb
import os

"""
print("Engine URL:", engine.url)
print("Banco usado:", os.path.abspath("todos.db"))
"""

app = FastAPI()
Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(getDb)]

@app.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_to_tasks():
    return RedirectResponse(url="/Tasks")

@app.get("/Tasks", status_code=status.HTTP_200_OK)
async def readAllEntries(db: db_dependency):
    return db.query(ToDosModel).all()

@app.get("/Tasks/{task_id}", status_code=status.HTTP_200_OK)
async def readTaskById(db:db_dependency, task_id:int):
    model =db.query(ToDosModel).filter(ToDosModel.id ==task_id).first()
    if(model is not None):
        return model
    raise HTTPException(status_code=404, detail="Task not found")