import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    assert response.url.path == "/static/index.html"

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_success():
    # Use an activity with empty participants initially
    response = client.post("/activities/Soccer%20Team/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "test@mergington.edu" in data["message"]

def test_signup_already_signed_up():
    # First signup
    client.post("/activities/Soccer%20Team/signup?email=test2@mergington.edu")
    # Try again
    response = client.post("/activities/Soccer%20Team/signup?email=test2@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    # First signup
    client.post("/activities/Basketball%20Club/signup?email=test3@mergington.edu")
    # Then unregister
    response = client.delete("/activities/Basketball%20Club/unregister?email=test3@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "test3@mergington.edu" in data["message"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Basketball%20Club/unregister?email=notsigned@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"]

def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]