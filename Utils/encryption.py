from passlib.context import CryptContext
#Passlib 1.7.4 + bcrypt 4.1.2 (💥 breaks)
#Passlib 1.7.4 + bcrypt 4.0.1 (✅ works — sweet spot)
from jose import jwt
from datetime import timedelta, datetime, timezone

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
    
    @classmethod
    def createAccessToken(cls, username:str, user_id:int, exp: timedelta):
        encode = {'sub': username, "id": user_id}
        expires = datetime.now(timezone.utc) + exp
        encode.update({'exp':expires})
        return jwt.encode(encode, cls.SECRET_KEY, cls.ALGORITHM)