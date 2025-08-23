from Utils.testsReusables import *
from fastapi import status


client = getTestClient()

def testGetUser(testUser):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    # make sure the response contains the same values as the fixture
    assert data["email"] == "charlie@example.com"
    assert data["username"] == "charlie99"
    assert data["first_name"] == "Charlie"
    assert data["last_name"] == "Brown"
    assert data["is_active"] is True
    assert data["role"] == "admin"
    assert data["phone_number"] == "+55 21 98888-7777"

    # id should exist and match the DB object
    assert data["id"] == testUser.id

def testChangeUserPassword(testUser):
    response = client.put("/user/password", json={"password": "testPassword", 
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
def testChangeUserInvalidPassword(testUser):
    response = client.put("/user/password", json={"password": "notThePassword", 
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail" : "Could not confirm password."
    }
    
def testChangeUserPhone(testUser):
    new_phone = "+5511987654321"
    response = client.put(
        "/user/phone",
        json={"new_phone": new_phone}
    )

    assert response.status_code == status.HTTP_202_ACCEPTED

    # Check the DB was updated
    db = TestingSessionLocal()
    user_db = db.query(UsersModel).filter_by(id=testUser.id).first()
    assert user_db.phone_number == new_phone