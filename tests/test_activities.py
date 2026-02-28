from urllib.parse import quote

from src import app as application


def test_signup_success(client):
    email = "newperson@mergington.edu"
    activity = "Chess Club"
    url = f"/activities/{quote(activity)}/signup?email={quote(email)}"
    response = client.post(url)
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    assert email in application.activities[activity]["participants"]


def test_signup_nonexistent(client):
    response = client.post("/activities/NoSuch/signup?email=a@b.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate(client):
    existing = application.activities["Chess Club"]["participants"][0]
    activity = "Chess Club"
    url = f"/activities/{quote(activity)}/signup?email={quote(existing)}"
    response = client.post(url)
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_missing_email(client):
    url = f"/activities/{quote('Chess Club')}/signup"
    response = client.post(url)
    assert response.status_code == 422


def test_unenroll_success(client):
    activity = "Gym Class"
    email = application.activities[activity]["participants"][0]
    url = f"/activities/{quote(activity)}/unenroll?email={quote(email)}"
    response = client.post(url)
    assert response.status_code == 200
    assert response.json()["message"] == f"Unenrolled {email} from {activity}"
    assert email not in application.activities[activity]["participants"]


def test_unenroll_not_enrolled(client):
    url = f"/activities/{quote('Gym Class')}/unenroll?email={quote('not@here.com')}"
    response = client.post(url)
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unenroll_nonexistent(client):
    response = client.post("/activities/Nope/unenroll?email=x@x.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
