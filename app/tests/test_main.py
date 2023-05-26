from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_check_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == 'Welcome to NQueens Puzzle Optimizations!'
