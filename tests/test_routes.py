import json
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_create_project_missing_app_name(client):
    response = client.post('/projects', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_create_project_valid(client):
    response = client.post('/projects', json={"app_name": "MyCoolApp"})
    assert response.status_code == 202
    data = response.get_json()
    assert "job_id" in data
    assert "celery_task_id" in data
