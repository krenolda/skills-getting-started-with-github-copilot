import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setitem(
        activities,
        "Test Activity",
        {
            "description": "Activity used by the unregister tests",
            "schedule": "Fridays",
            "max_participants": 2,
            "participants": ["student@mergington.edu"],
        },
    )
    return TestClient(app)


def test_unregister_removes_participant(client):
    response = client.delete(
        "/activities/Test%20Activity/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered student@mergington.edu from Test Activity"
    }
    assert activities["Test Activity"]["participants"] == []


def test_unregister_returns_not_found_for_missing_participant(client):
    response = client.delete(
        "/activities/Test%20Activity/participants",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
