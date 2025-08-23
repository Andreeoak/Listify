from Utils.testsReusables import *
from Utils.encryption import jwtEncryption
from routers.auth import authenticate_user
from fastapi import status
from datetime import timedelta
from jose import jwt

"""
router = APIRouter(
prefix='/auth',
tags=['Auth']
)
db_dependency = Annotated[Session, Depends(getDb)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def createUser(db:db_dependency, createUserRequest: UserInterface):
create_user_model = UsersModel(
    email = createUserRequest.email,
    username = createUserRequest.username,
    first_name = createUserRequest.first_name,
    last_name= createUserRequest.last_name,
    role = createUserRequest.role,
    phone_number = createUserRequest.phone_number,
    hashed_password = EncryptionContext.hashPassword(createUserRequest.password),
    is_active = True
)
db.add(create_user_model)
db.commit()
db.refresh(create_user_model)
return{ 
    "Message": "User created succesfully!",
    "User":   create_user_model 
}

@router.post("/token", response_model=TokenInterface)
async def loginForAccessToken(
form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
db: db_dependency):
user = authenticate_user(form_data.username, form_data.password, db)
if(not user):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify credentials")
token = jwtEncryption.createAccessToken(user.username, user.id, user.role, timedelta(minutes=20))
return {'access_token':token, "token_type": 'bearer'}
"""

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