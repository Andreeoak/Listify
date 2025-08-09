from fastapi import FastAPI
from routers import auth, toDos
from Database.database import engine, Base

app = FastAPI()
Base.metadata.create_all(bind=engine) 
app.include_router(auth.router)
app.include_router(toDos.router)