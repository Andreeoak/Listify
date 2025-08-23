from main import app
from Database.MockDatabase import override_getDb
from Utils.encryption import jwtEncryption, EncryptionContext as Encrypt
from fastapi.testclient import TestClient
from Database.database import getDb
from Database.Models.ToDosModel import ToDosModel
from Database.Models.UsersModel import UsersModel
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
        
@pytest.fixture
def testUser():
    mock_user = UsersModel(
        email="charlie@example.com",
        username="charlie99",
        first_name="Charlie",
        last_name="Brown",
        hashed_password= Encrypt.hashPassword("testPassword"),
        is_active=True,
        role="admin",
        phone_number="+55 21 98888-7777"
    )
    db = TestingSessionLocal()
    db.add(mock_user)
    db.commit()
    db.refresh(mock_user)  # refresh to get auto-generated ID
    yield mock_user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.execute(text("DELETE FROM users;"))  # clean up user too
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
