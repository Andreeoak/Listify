from sqlalchemy import text
from Database.MockDatabase import TestingSessionLocal, engine
from fastapi import status
import pytest
from Database.Models.ToDosModel import ToDosModel
from Utils.testsReusables import getTestClient

Client = getTestClient()

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
    
def testUpdateTaskNotFound(testTodo):
    request_data = {
        'title': 'Change the title of the todo already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }

    # URL corrigida
    response = Client.put("/Tasks/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
            "detail": "Task not found"
        }
    

def testDeleteTask(testTodo):
    response = Client.delete('/Tasks/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(ToDosModel).filter(ToDosModel==1).first()
    assert model is None
    
def testDeleteTaskNotFound(testTodo):
    response = Client.delete('/Tasks/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
            "detail": "Task not found"
        }