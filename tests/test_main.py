from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo à API de Tarefas!"}

def test_preflight_request():
    response = client.options("/some-path")
    assert response.status_code == 200
    assert response.json() == {"message": "Preflight request successful"}
