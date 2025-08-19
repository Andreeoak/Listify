from fastapi.testclient import TestClient
from fastapi import status
import main

client = TestClient(main.app)

def testHealthCheckHTTPResponse():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK, "Normal response is HTTP 200 - OK"
    
def testHealthCheckJsonResponse():
    response = client.get("/health")
    assert response.json() == {'status': 'Healthy'}, "Expected response is that the server is Healthy"