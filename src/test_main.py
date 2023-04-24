from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_check_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ['Ok! All set guys!']

