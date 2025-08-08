from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = 'sqlite:///todos.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False})
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base() # creates a base class that will be used to define ORM models

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()