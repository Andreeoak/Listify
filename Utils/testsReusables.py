from main import app
from Database.MockDatabase import override_getDb
from Utils.encryption import jwtEncryption
from fastapi.testclient import TestClient
from Database.database import getDb
from Database.Models.ToDosModel import ToDosModel
from Database.MockDatabase import TestingSessionLocal, engine
from sqlalchemy import text
import pytest


async def override_get_current_user():
    return {
        "username": "andreCarvalho",
        "id": 1,
        "user_role": "admin"
    }

def getTestClient():
    app.dependency_overrides[getDb] = override_getDb
    app.dependency_overrides[jwtEncryption.getCurrentUser] = override_get_current_user

    return TestClient(app)

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


async def override_get_current_user_with_non_admin():
    return {
        "username": "andreCarvalho",
        "id": 1,
        "user_role": "user"
    }
    
def getTestClientForNonAdmin():
    app.dependency_overrides[getDb] = override_getDb
    app.dependency_overrides[jwtEncryption.getCurrentUser] = override_get_current_user_with_non_admin

    return TestClient(app)
