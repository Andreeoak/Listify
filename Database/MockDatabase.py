from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///testdb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, 
                        connect_args={
                            'check_same_thread':False
                            },
                        poolclass=StaticPool
                       )

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_getDb():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
