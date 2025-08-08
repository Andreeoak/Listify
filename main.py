from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from Database.Models.ToDosModel import ToDosModel
from Database.database import engine, SessionLocal, Base, getDb
import os

"""
print("Engine URL:", engine.url)
print("Banco usado:", os.path.abspath("todos.db"))
"""

app = FastAPI()
Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(getDb)]

@app.get("/")
async def readAllEntries(db: db_dependency):
    return db.query(ToDosModel).all()