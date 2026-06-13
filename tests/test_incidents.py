from fastapi.testclient import TestClient
from app.main import app, incidents

client = TestClient(app)

def setup_function():
    incidents.clear()

def test_create_incident_successfully():
    response = client.post(
        "/incidents",
        json={
            "title": "Payment API timeout",
            "description": "Users cannot complete payments",
            "severity": "high",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Payment API timeout"
    assert data["description"] == "Users cannot complete payments"
    assert data["severity"] == "high"
    assert data["status"] == "open"


def test_invalid_severity_returns_400():
    response = client.post(
        "/incidents",
        json={
            "title": "Payment API timeout",
            "description": "Users cannot complete payments",
            "severity": "banana",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Invalid severity. Allowed values are: low, medium, high, critical"
    )


def test_get_missing_incident_returns_404():
    response = client.get("/incidents/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Incident not found"


def test_update_status_successfully():
    create_response = client.post(
        "/incidents",
        json={
            "title": "Login broken",
            "description": "Users cannot log in",
            "severity": "critical",
        },
    )

    incident_id = create_response.json()["id"]

    update_response = client.patch(
        f"/incidents/{incident_id}/status",
        json={"status": "investigating"},
    )

    assert update_response.status_code == 200
    assert update_response.json()["status"] == "investigating"


def test_invalid_status_returns_400():
    create_response = client.post(
        "/incidents",
        json={
            "title": "Login broken",
            "description": "Users cannot log in",
            "severity": "critical",
        },
    )

    incident_id = create_response.json()["id"]

    update_response = client.patch(
        f"/incidents/{incident_id}/status",
        json={"status": "banana"},
    )

    assert update_response.status_code == 400
    assert update_response.json()["detail"] == (
        "Invalid status. Allowed values are: open, investigating, resolved, closed"
    )