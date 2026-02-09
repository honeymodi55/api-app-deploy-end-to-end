import pytest
from fastapi.testclient import TestClient
from app import app

# Initialize the TestClient with the FastAPI app
client = TestClient(app)

def test_read_root():
    """Test the HTML root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "<h1>Hello, World!</h1>" in response.text

def test_hello_api():
    """Test the JSON API endpoint"""
    response = client.get("/api/hello")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello, World!"
    assert data["status"] == "success"

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}