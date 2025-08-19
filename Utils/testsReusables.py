from sqlalchemy import text
from main import app
from Database.MockDatabase import override_getDb
from Utils.encryption import jwtEncryption
from fastapi.testclient import TestClient
from Database.database import getDb


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