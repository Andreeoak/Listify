from main import app
from Database.MockDatabase import override_getDb
from routers.toDos import getDb
from Utils.encryption import jwtEncryption
from fastapi.testclient import TestClient
from fastapi import status

def override_get_current_user():
    return {
        "username": "andreCarvalho",
        "id": 1,
        "user_role": "admin"
    }


app.dependency_overrides[getDb] = override_getDb
app.dependency_overrides[jwtEncryption.getCurrentUser] = override_get_current_user

Client = TestClient(app)

def testReadAllAuthenticated():
    response = Client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    