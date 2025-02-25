from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo à API de Tarefas!"}

def test_read_tasks():
    response = client.get("/api/tasks")
    assert response.status_code == 200
    # Add more assertions based on the expected response from the /api/tasks endpoint