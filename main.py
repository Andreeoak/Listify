from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from routers import auth, toDos, admin, users
from Database.database import engine, Base
# Importar modelos antes de criar tabelas
from Database.Models.UsersModel import UsersModel
from Database.Models.ToDosModel import ToDosModel

app = FastAPI()
Base.metadata.create_all(bind=engine) 

app.mount("/static", StaticFiles(directory="Templates/Static"), name= "static")

@app.get("/")
def test(request: Request):
    return RedirectResponse("/todos/todo-page", status_code=status.HTTP_302_FOUND)

@app.get("/health")
def healthCheck():
    return{
        'status': 'Healthy'
    }
    
app.include_router(auth.router)
app.include_router(toDos.router)
app.include_router(admin.router)
app.include_router(users.router)