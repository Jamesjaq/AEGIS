import pytest
import os
import sys
# Add unified-api to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "unified-api")))

from bridge import app
from database.manager import init_db
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_health():
    init_db()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "aegis-unified-api"}

@patch("httpx.AsyncClient.get")
def test_stream_endpoint(mock_get):
    init_db()
    # Mock ShadowBroker response
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "commercial_flights": [{"icao24": "abc", "lat": 10, "lon": 20}],
        "ships": []
    }
    mock_get.return_value = mock_resp

    response = client.get("/api/stream")
    assert response.status_code == 200
    data = response.json()
    assert "entities" in data
    assert len(data["entities"]) > 0
    assert data["entities"][0]["id"] == "flight-abc"
    assert "intelligence" in data
