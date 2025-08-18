from fastapi import FastAPI
from routers import auth, toDos, admin, users
from Database.database import engine, Base
# Importar modelos antes de criar tabelas
from Database.Models.UsersModel import UsersModel
from Database.Models.ToDosModel import ToDosModel

app = FastAPI()
Base.metadata.create_all(bind=engine) 

@app.get("/health")
def healthCheck():
    return{
        'status': 'Healthy'
    }
    
app.include_router(auth.router)
app.include_router(toDos.router)
app.include_router(admin.router)
app.include_router(users.router)