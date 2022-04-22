from starlette.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_alive():
    response = client.get('/')

    assert response.status_code == 200
    assert response.json().get('message') == 'Fast API Server'


def test_get_matches():
    response = client.get('/matches')
    assert response.status_code == 200
    assert len(response.json()) != 0


def test_add_opportunities():
    response = client.post('/opportunities')
    assert response.status_code == 200
    assert len(response.json()) != 0

def test_add_users():
    response = client.post('/users')
    assert response.status_code == 200
    assert len(response.json()) != 0

def test_read_question_invalid():
    response = client.get('/Foobar')
    assert response.status_code == 404
    