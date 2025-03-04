from fastapi.testclient import TestClient
from app.main import app
import boto3
from moto import mock_aws
import pytest

client = TestClient(app)

@pytest.fixture(scope='function')
def dynamodb_mock():
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        yield dynamodb

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo à API de Tarefas!"}

def test_preflight_request():
    response = client.options("/some-path")
    assert response.status_code == 200
    assert response.json() == {"message": "Preflight request successful"}