import pytest
from fastapi.testclient import TestClient
from app.routers.tasks_router import tasks_router
from app.models import Task, UpdateTaskModel
from app.db import db

client = TestClient(tasks_router)

def test_create_task_success():
    task_data = {"name": "Test Task", "description": "Test Description"}
    response = client.post("/", json=task_data)
    assert response.status_code == 201
    assert response.json()["name"] == task_data["name"]

def test_create_task_failure():
    response = client.post("/", json={})
    assert response.status_code == 500

def test_get_task_success():
    task_data = {"name": "Test Task", "description": "Test Description"}
    create_response = client.post("/", json=task_data)
    task_id = create_response.json()["id"]
    
    response = client.get(f"/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_get_task_not_found():
    response = client.get("/999")
    assert response.status_code == 404

def test_get_tasks_success():
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json()["tasks"], list)

def test_update_task_success():
    task_data = {"name": "Test Task", "description": "Test Description"}
    create_response = client.post("/", json=task_data)
    task_id = create_response.json()["id"]
    
    update_data = {"name": "Updated Task", "description": "Updated Description"}
    response = client.put(f"/{task_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]

def test_update_task_not_found():
    update_data = {"name": "Updated Task", "description": "Updated Description"}
    response = client.put("/999", json=update_data)
    assert response.status_code == 404

def test_delete_task_success():
    task_data = {"name": "Test Task", "description": "Test Description"}
    create_response = client.post("/", json=task_data)
    task_id = create_response.json()["id"]
    
    response = client.delete(f"/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}

def test_delete_task_not_found():
    response = client.delete("/999")
    assert response.status_code == 200

def test_delete_all_tasks():
    response = client.delete("/")
    assert response.status_code == 200
    assert response.json() == {"message": "All tasks deleted successfully"}  
