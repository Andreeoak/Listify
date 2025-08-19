from sqlalchemy import text
from main import app
from Database.MockDatabase import override_getDb, TestingSessionLocal, engine
from routers.toDos import getDb
from Utils.encryption import jwtEncryption
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from Database.Models.ToDosModel import ToDosModel

async def override_get_current_user():
    return {
        "username": "andreCarvalho",
        "id": 1,
        "user_role": "admin"
    }


app.dependency_overrides[getDb] = override_getDb
app.dependency_overrides[jwtEncryption.getCurrentUser] = override_get_current_user

Client = TestClient(app)

@pytest.fixture
def testTodo():
    todo = ToDosModel(
        title= "Learn to code!",
        description= "Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("Delete from todos;"))
        connection.commit()

def testReadAllAuthenticated(testTodo):
    response = Client.get("/Tasks")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "complete": False,
            "title": "Learn to code!",
            "description": "Need to learn everyday!",
            "id":1,
            "priority": 5,
            "owner_id":1
        }
    ]
    
def testReadTaskById(testTodo):
    response = Client.get("/Tasks/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
            "complete": False,
            "title": "Learn to code!",
            "description": "Need to learn everyday!",
            "id":1,
            "priority": 5,
            "owner_id":1
        }
    

def testReadTaskByIdNotFound(testTodo):
    response = Client.get("/Tasks/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
            "detail": "Task not found"
        }
    
def testCreateTask():
    request_data ={
        "title": "New Todo!",
        'description': "Todo description",
        'priority': 5,
        'complete': False
    }
    response = Client.post("/Tasks", json = request_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    db = TestingSessionLocal()
    model = db.query(ToDosModel).order_by(ToDosModel.id.desc()).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')
    
    
def testUpdateTask(testTodo):
    request_data = {
        'title': 'Change the title of the todo already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }

    # URL corrigida
    response = Client.put("/Tasks/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(ToDosModel).filter(ToDosModel.id == 1).first()
    assert model.title == request_data['title']