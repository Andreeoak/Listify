from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
from Database.Models.ToDosModel import ToDosModel
from Database.database import getDb
from Interfaces.TaskInterface import TaskInterface
from Utils.encryption import jwtEncryption
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="Templates")

router = APIRouter(
    prefix="/todos",
    tags=['todos']   
)

db_dependency = Annotated[Session, Depends(getDb)]
user_dependency = Annotated[dict, Depends(jwtEncryption.getCurrentUser)]

def redirect_to_login():
    redirect_response= RedirectResponse("/auth/login-page", status_code= status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response

### Mounting page
@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await jwtEncryption.getCurrentUser(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        todos = db.query(ToDosModel).filter(ToDosModel.owner_id==user.get("id")).all()
        return templates.TemplateResponse("todo.html", {"request":request, "todos":todos, "user":user})
    except:
        return redirect_to_login()
    
@router.get('/add-todo-page')
async def render_add_todo_page(request: Request, db:db_dependency):
    try:
        user = await jwtEncryption.getCurrentUser(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse("add-todo.html", {"request":request, "user":user})
    except:
        return redirect_to_login()
    
@router.get('/edit-todo-page/{todo_id}')
async def render_edit_todo_page(request: Request, todo_id: int, db:db_dependency):
    try:
        user = await jwtEncryption.getCurrentUser(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        todo = db.query(ToDosModel).filter(ToDosModel.id==todo_id).first()
        return templates.TemplateResponse("edit-todo.html", {"request":request, "todo": todo, "user":user})
    except:
        return redirect_to_login()

### Endpoints

@router.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_to_tasks():
    return RedirectResponse(url="/Tasks")

@router.get("/Tasks", status_code=status.HTTP_200_OK)
async def readAllEntries(user:user_dependency, db: db_dependency):
    if(user is None):
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todos = db.query(ToDosModel).filter(ToDosModel.owner_id == user["id"]).all()
    return jsonable_encoder(todos, exclude={"owner": {"todos"}}) #lets you skip fields that cause recursion => just exclude the deep nesting in serialization.

@router.get("/Tasks/{task_id}", status_code=status.HTTP_200_OK)
async def readTaskById(user:user_dependency, db:db_dependency, task_id:int):
    if(user is None):
        raise HTTPException(status_code=401, detail="Authentication Failed")
    model =db.query(ToDosModel).filter(ToDosModel.id ==task_id).filter(ToDosModel.owner_id == user.get("id")).first()
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
async def updateTask(user:user_dependency, db: db_dependency, task_id:int, task:TaskInterface):
    if(user is None):
        raise HTTPException(status_code=401, detail="Authentication Failed")
    model = db.query(ToDosModel).filter(ToDosModel.id == task_id).filter(ToDosModel.owner_id == user.get("id")).first()
    if model is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(model, key, value)
    db.commit()
    
@router.delete("/Tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTask(user: user_dependency, db: db_dependency, task_id:int):
    if(user is None):
        raise HTTPException(status_code=401, detail="Authentication Failed")
    model = db.query(ToDosModel).filter(ToDosModel.id == task_id).filter(ToDosModel.owner_id == user.get("id")).first()
    if model is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.query(ToDosModel).filter(ToDosModel.id == task_id).delete()
    db.commit()
        