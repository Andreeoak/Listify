from fastapi import FastAPI

import Database.Models.ToDosModel as Models
from Database.database import engine

app = FastAPI()

Models.Base.metadata.create_all(bind=engine)