import pytest
from app import app
import uuid

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Health check
def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"message": "User Management System is up"}


# Create user (missing fields)
def test_create_user_missing_fields(client):
    data = {"email": "no-name@example.com"}
    response = client.post('/users', json=data)
    assert response.status_code == 400


# Login user (valid credentials)
def test_login_user(client):
    email = f"login_{uuid.uuid4()}@example.com"
    password = "Login123"

    # First create user
    create_resp = client.post('/users', json={
        "name": "Login User",
        "email": email,
        "password": password
    })
    assert create_resp.status_code == 201

    # Then login
    response = client.post('/login', json={
        "email": email,
        "password": password
    })
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['status'] == "success"
    assert 'user_id' in json_data


# Login user (wrong password)
def test_login_user_wrong_password(client):
    email = f"loginfail_{uuid.uuid4()}@example.com"

    # Create user
    client.post('/users', json={
        "name": "Wrong Pass",
        "email": email,
        "password": "CorrectPass"
    })

    # Attempt with wrong password
    response = client.post('/login', json={
        "email": email,
        "password": "WrongPass"
    })
    assert response.status_code == 401


# Get all users
def test_get_all_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


# Get user not found
def test_get_non_existing_user(client):
    response = client.get('/user/999999')
    assert response.status_code == 404
