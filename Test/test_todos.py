from main import app
from Database.database import getDb
from Database.MockDatabase import override_getDb

app.dependency_overrides[getDb] = override_getDb