from Utils.testsReusables import *
from fastapi import status



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
    