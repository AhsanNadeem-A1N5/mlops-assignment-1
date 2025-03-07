import pytest
import json
from app import app  # Import the Flask app

@pytest.fixture
def client():
    """Fixture to set up the test client."""
    app.testing = True  # Enable testing mode
    client = app.test_client()
    return client

def test_home(client):
    """Test the home route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the K-Means Model Training API!" in response.data

def test_train(client):
    """Test the train model route."""
    response = client.get('/train')
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Model trained successfully!"
    assert "cluster_centers" in data
    assert isinstance(data["cluster_centers"], list)

def test_predict_valid(client):
    """Test the predict route with a valid input."""
    payload = {"type": "setosa"}
    response = client.post('/predict', data=json.dumps(payload), content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert "type" in data
    assert data["type"] == "setosa"
    assert "average_features" in data
    assert all(key in data["average_features"] for key in ["sepal_length", "sepal_width", "petal_length", "petal_width"])

def test_predict_invalid(client):
    """Test the predict route with an invalid input."""
    payload = {"type": "unknown"}
    response = client.post('/predict', data=json.dumps(payload), content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid type. Choose from setosa, versicolor, or virginica."

def test_predict_missing_key(client):
    """Test the predict route with missing key in JSON."""
    payload = {}  # No "type" key
    response = client.post('/predict', data=json.dumps(payload), content_type='application/json')
    
    assert response.status_code == 400  # Expecting a bad request
    data = response.get_json()
    assert "error" in data

if __name__ == "__main__":
    pytest.main()
