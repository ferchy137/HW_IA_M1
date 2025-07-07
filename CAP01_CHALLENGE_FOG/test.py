"""
Test suite for user authentication and data manipulation API endpoints.

This module contains unit tests for:
- User registration and login functionality
- Authentication token validation
- Various data manipulation endpoints (bubble sort, filtering, searching, etc.)

Tests cover successful and failure scenarios for:
- User registration with new and existing usernames
- Login with valid and invalid credentials
- Authorized and unauthorized access to protected endpoints
- Correct implementation of data manipulation algorithms
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from main import app, fake_db, get_password_hash

client = TestClient(app)

def test_register_new_user():
    fake_db["users"] = {}
    response = client.post("/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}
    assert "testuser" in fake_db["users"]
    assert "password" in fake_db["users"]["testuser"]

def test_register_existing_user():
    fake_db["users"] = {"existinguser": {"password": "hashedpass"}}
    response = client.post("/register", json={"username": "existinguser", "password": "testpass"})
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"

def test_login_success():
    hashed_password = get_password_hash("testpass")
    fake_db["users"] = {"testuser": {"password": hashed_password}}
    response = client.post("/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_username():
    fake_db["users"] = {}
    response = client.post("/login", json={"username": "nonexistent", "password": "testpass"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_login_invalid_password():
    hashed_password = get_password_hash("rightpass")
    fake_db["users"] = {"testuser": {"password": hashed_password}}
    response = client.post("/login", json={"username": "testuser", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_bubble_sort():
    token = client.post("/login", json={"username": "testuser", "password": "testpass"}).json()["access_token"]
    response = client.post("/bubble-sort", json={"numbers": [4,2,1,3]}, headers={"token": token})
    assert response.status_code == 200
    assert response.json() == {"numbers": [1,2,3,4]}

def test_filter_even():
    token = client.post("/login", json={"username": "testuser", "password": "testpass"}).json()["access_token"]
    response = client.post("/filter-even", json={"numbers": [1,2,3,4,5,6]}, headers={"token": token})
    assert response.status_code == 200
    assert response.json() == {"even_numbers": [2,4,6]}

def test_sum_elements():
    token = client.post("/login", json={"username": "testuser", "password": "testpass"}).json()["access_token"]
    response = client.post("/sum-elements", json={"numbers": [1,2,3,4,5]}, headers={"token": token})
    assert response.status_code == 200
    assert response.json() == {"sum": 15}

def test_max_value():
    token = client.post("/login", json={"username": "testuser", "password": "testpass"}).json()["access_token"]
    response = client.post("/max-value", json={"numbers": [1,5,3,9,2]}, headers={"token": token})
    assert response.status_code == 200
    assert response.json() == {"max": 9}

def test_binary_search_found():
    token = client.post("/login", json={"username": "testuser", "password": "testpass"}).json()["access_token"]
    response = client.post("/binary-search", json={"numbers": [1,2,3,4,5], "target": 3}, headers={"token": token})
    assert response.status_code == 200
    assert response.json() == {"found": True, "index": 2}

def test_binary_search_not_found():
    token = client.post("/login", json={"username": "testuser", "password": "testpass"}).json()["access_token"]
    response = client.post("/binary-search", json={"numbers": [1,2,3,4,5], "target": 6}, headers={"token": token})
    assert response.status_code == 200
    assert response.json() == {"found": False, "index": -1}

def test_unauthorized_access():
    response = client.post("/bubble-sort", json={"numbers": [4,2,1,3]}, headers={"token": "invalid_token"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"
