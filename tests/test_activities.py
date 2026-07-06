import urllib.parse


def test_get_activities_returns_dict(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant(client):
    email = "tester@example.com"
    activity = "Chess Club"
    url = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"

    resp = client.post(url)
    assert resp.status_code == 200

    data = client.get("/activities").json()
    assert email in data[activity]["participants"]


def test_duplicate_signup_returns_400(client):
    email = "duplicate@example.com"
    activity = "Chess Club"
    url = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"

    r1 = client.post(url)
    assert r1.status_code == 200

    r2 = client.post(url)
    assert r2.status_code == 400


def test_remove_participant(client):
    activity = "Chess Club"
    # use an existing participant from the seed data
    email = "michael@mergington.edu"

    del_url = f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(email)}"
    resp = client.delete(del_url)
    assert resp.status_code == 200

    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]


def test_signup_for_nonexistent_activity_returns_404(client):
    resp = client.post("/activities/NoSuchActivity/signup?email=noone@example.com")
    assert resp.status_code == 404


def test_remove_nonexistent_participant_returns_404(client):
    activity = "Chess Club"
    email = "not-a-person@example.com"
    del_url = f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(email)}"
    resp = client.delete(del_url)
    assert resp.status_code == 404
