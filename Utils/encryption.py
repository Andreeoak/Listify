from passlib.context import CryptContext
#Passlib 1.7.4 + bcrypt 4.1.2 (💥 breaks)
#Passlib 1.7.4 + bcrypt 4.0.1 (✅ works — sweet spot)
from jose import jwt, JWSError
from datetime import timedelta, datetime, timezone
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException, status

class EncryptionContext:
    # Create only once at import time
    _bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @classmethod
    def hashPassword(cls, password: str):
        return cls._bcrypt_context.hash(password)
    
    @classmethod
    def verifyPassword(cls, plain_password: str, hashed_password: str):
        return cls._bcrypt_context.verify(plain_password, hashed_password)
    
class jwtEncryption:
    SECRET_KEY = '69905614fb3c9e2b433ae26e9e198660da6d9daedbe8a9e63669aae008db7095'
    ALGORITHM = 'HS256'
    oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
    
    @classmethod
    def createAccessToken(cls, username:str, user_id:int, exp: timedelta):
        encode = {'sub': username, "id": user_id}
        expires = datetime.now(timezone.utc) + exp
        encode.update({'exp':expires})
        return jwt.encode(encode, cls.SECRET_KEY, cls.ALGORITHM)
    
    @classmethod
    async def getCurrentUser(cls, token: Annotated[str, Depends(oauth2_bearer)]):
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            username:str = payload.get('sub')
            user_id: int = payload.get('id')
            if username is None or user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify credentials")
            return {"username":username, "id":user_id}
        except JWSError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify credentials")