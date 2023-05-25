from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_check_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == 'Welcome to NQueens Puzzle Optimizations!'


def test_check_nqueens():
    response = client.get("/backtracking/4")
    assert response.status_code == 200

    #data = response.json()
    #assert data["elapsed_time"] > 0
    #assert data["number_of_solutions"] == 2
