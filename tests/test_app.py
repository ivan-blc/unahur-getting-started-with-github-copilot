def test_root_redirect(client):
    response = client.get("/")
    # The app may either redirect to the static index or serve it directly.
    assert response.status_code in (200, 302, 307)
    if response.status_code in (302, 307):
        assert response.headers.get("location") == "/static/index.html"
    else:
        # served content should contain the page title
        assert "Mergington High School" in response.text


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    # should contain at least one activity and have the expected structure
    assert isinstance(data, dict)
    assert "Chess Club" in data
    sample = data["Chess Club"]
    assert "description" in sample
    assert "schedule" in sample
    assert "max_participants" in sample
    assert "participants" in sample
