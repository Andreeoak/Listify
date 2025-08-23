from Utils.testsReusables import *
from fastapi import status
from Database.Models.ToDosModel import ToDosModel



def testGetAllTasksForAdmin(testTodo):
    Client = getTestClient()
    response = Client.get("/admin/todo")
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

    
def testGetAllTasksForNonAdmin(testTodo):
    NonAdmin = getTestClientForNonAdmin()
    response = NonAdmin.get("/admin/todo")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        'detail': "Authentication Failed!"
    }
    
def testDeleteTaskByID(testTodo):
    response = Client = getTestClient()
    response = Client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(ToDosModel).filter(ToDosModel.id == 1).first()
    assert(model is None)
    
def testDeleteTaskByIDNotFOund(testTodo):
    response = Client = getTestClient()
    response = Client.delete("/admin/todo/13199")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "No records found with id= 13199"
    }
    