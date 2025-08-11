from passlib.context import CryptContext
#Passlib 1.7.4 + bcrypt 4.1.2 (💥 breaks)
#Passlib 1.7.4 + bcrypt 4.0.1 (✅ works — sweet spot)

class EncryptionContext:
    # Create only once at import time
    _bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @classmethod
    def hashPassword(cls, password: str):
        return cls._bcrypt_context.hash(password)
    
    @classmethod
    def verifyPassword(cls, plain_password: str, hashed_password: str):
        return cls._bcrypt_context.verify(plain_password, hashed_password)