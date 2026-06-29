from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import activities as activities_store


def test_get_activities(client: TestClient):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert activity_name in data
    assert "description" in data[activity_name]
    assert "participants" in data[activity_name]


def test_signup_adds_participant(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_participants = list(activities_store[activity_name]["participants"])
    url_activity = quote(activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{url_activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert activities_store[activity_name]["participants"] == initial_participants + [email]


def test_duplicate_signup_returns_400(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = activities_store[activity_name]["participants"][0]
    initial_count = len(activities_store[activity_name]["participants"])
    url_activity = quote(activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{url_activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert len(activities_store[activity_name]["participants"]) == initial_count


def test_remove_participant(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = activities_store[activity_name]["participants"][0]
    initial_participants = list(activities_store[activity_name]["participants"])
    url_activity = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{url_activity}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities_store[activity_name]["participants"]
    assert len(activities_store[activity_name]["participants"]) == len(initial_participants) - 1


def test_remove_missing_participant_returns_404(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "missing.student@mergington.edu"
    url_activity = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{url_activity}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
