import json
import pytest
from unittest.mock import patch, Mock
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_project_missing_app_name(client):
    response = client.post('/projects', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

@patch('app.routes.build_project_task')
@patch('app.config.load_config')
def test_create_project_valid(mock_config, mock_task, client):
    # Mock the config
    mock_config.return_value = {
        "REDIS_URL": "redis://localhost:6379/0",
        "GITHUB_TOKEN": "test_token",
        "GITHUB_ORG": "test_org",
    }
    
    # Mock the Celery task
    mock_async_result = Mock()
    mock_async_result.id = "mock-task-id"
    mock_task.apply_async.return_value = mock_async_result
    
    response = client.post('/projects', json={"app_name": "MyCoolApp"})
    assert response.status_code == 202
    data = response.get_json()
    assert "job_id" in data
    assert "celery_task_id" in data
    assert data["celery_task_id"] == "mock-task-id"
