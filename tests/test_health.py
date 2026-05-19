"""
Tests for the cloud-platform-service endpoints.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200


def test_health_fields():
    response = client.get("/health")
    body = response.json()
    assert body["status"] == "healthy"
    assert body["service"] == "cloud-platform-service"
    assert "version" in body
    assert "timestamp" in body
    assert "uptime_seconds" in body


def test_ready_returns_200():
    response = client.get("/ready")
    assert response.status_code == 200


def test_ready_fields():
    response = client.get("/ready")
    body = response.json()
    assert body["ready"] is True
    assert "checks" in body


def test_metrics_returns_200():
    response = client.get("/metrics")
    assert response.status_code == 200


def test_metrics_fields():
    response = client.get("/metrics")
    body = response.json()
    assert "counters" in body
    assert "uptime_seconds" in body


def test_simulate_error_returns_500():
    response = client.get("/simulate-error")
    assert response.status_code == 500


def test_simulate_error_fields():
    response = client.get("/simulate-error")
    body = response.json()
    assert body["error"] == "SimulatedError"
    assert "request_id" in body
    assert "timestamp" in body
