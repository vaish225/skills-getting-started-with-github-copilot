import urllib.parse


def test_get_activities_returns_dict(client):
    # Arrange: none (use seeded data)
    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant(client):
    # Arrange
    email = "tester@example.com"
    activity = "Chess Club"
    url = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"

    # Act
    resp = client.post(url)

    # Assert
    assert resp.status_code == 200
    data = client.get("/activities").json()
    assert email in data[activity]["participants"]


def test_duplicate_signup_returns_400(client):
    # Arrange
    email = "duplicate@example.com"
    activity = "Chess Club"
    url = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"

    # Act
    first = client.post(url)
    second = client.post(url)

    # Assert
    assert first.status_code == 200
    assert second.status_code == 400


def test_remove_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # seeded participant
    del_url = f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(email)}"

    # Act
    resp = client.delete(del_url)

    # Assert
    assert resp.status_code == 200
    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]


def test_signup_for_nonexistent_activity_returns_404(client):
    # Arrange
    url = "/activities/NoSuchActivity/signup?email=noone@example.com"

    # Act
    resp = client.post(url)

    # Assert
    assert resp.status_code == 404


def test_remove_nonexistent_participant_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "not-a-person@example.com"
    del_url = f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(email)}"

    # Act
    resp = client.delete(del_url)

    # Assert
    assert resp.status_code == 404
