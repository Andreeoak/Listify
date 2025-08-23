from Utils.testsReusables import *
from Utils.encryption import jwtEncryption
from routers.auth import authenticate_user
from fastapi import status, HTTPException
from datetime import timedelta
from jose import jwt


client = getTestClient()

def testAuthenticateUser(testUser):
    db = TestingSessionLocal()
    authenticatedUser = authenticate_user(testUser.username, "testPassword", db)
    
    assert authenticatedUser is not None
    assert authenticatedUser.username == testUser.username
    
def testAuthenticateUserInvalidPassword(testUser):
    db = TestingSessionLocal()
    authenticatedUser = authenticate_user(testUser.username, "wrongpassword", db)

    assert authenticatedUser is False
    
def testCreateAccessToken():
    username = 'testUser'
    user_id = 4
    role = 'user'
    expires_delta = timedelta(days=1)
    
    token = jwtEncryption.createAccessToken(username, user_id, role, expires_delta)
    decoded_token= jwt.decode(token, jwtEncryption.SECRET_KEY, jwtEncryption.ALGORITHM, options={'verify_signature': False})
    
    assert decoded_token['sub'] == username
    assert decoded_token['id']  == user_id
    assert decoded_token['role']  == role

@pytest.mark.asyncio
async def testGetCurrentUser():
    username = 'testUser'
    user_id = 4
    role = 'admin'
    encode = {'sub': username, "id": user_id, 'role':role}
    token = jwt.encode(encode, jwtEncryption.SECRET_KEY, jwtEncryption.ALGORITHM)
    
    user = await jwtEncryption.getCurrentUser(token)
    
    assert user == {"username": username, "id": user_id, "user_role": role}
    
    
@pytest.mark.asyncio
async def testGetCurrentUserMissingPayload():
    user_id = 4
    role = 'admin'
    encode = {"id": user_id, 'role':role}
    token = jwt.encode(encode, jwtEncryption.SECRET_KEY, jwtEncryption.ALGORITHM)
    
    with pytest.raises(HTTPException) as exceptionInfo:
        user = await jwtEncryption.getCurrentUser(token)
    
    assert exceptionInfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exceptionInfo.value.detail == "Could not verify credentials"