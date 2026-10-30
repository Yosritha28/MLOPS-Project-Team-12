from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
API = "/api/v1"


def test_scoring_config_is_stub_and_weights_sum_to_one():
    r = client.get(f"{API}/config/scoring")
    assert r.status_code == 200 and r.headers["x-stub"] == "true"
    w = r.json()["weights"]
    assert abs(w["tfidf"] + w["sbert"] + w["skills"] - 1) < 0.001


def test_scoring_update_rejects_weights_that_do_not_sum_to_one():
    body = {"weights": {"tfidf": 0.5, "sbert": 0.5, "skills": 0.5}}
    assert client.patch(f"{API}/admin/config/scoring", json=body).status_code == 422


def test_resume_upload_stub():
    files = {"file": ("cv.pdf", b"%PDF-1.4 test", "application/pdf")}
    r = client.post(f"{API}/resumes", files=files)
    assert r.status_code == 201 and r.json()["filename"] == "cv.pdf"


def test_recommended_route_is_not_swallowed_by_job_id():
    r = client.get(f"{API}/jobs/recommended")
    assert r.status_code == 200 and isinstance(r.json(), list)


def test_job_create_accepts_custom_fields():
    body = {
        "title": "Data Engineer",
        "description": "Build pipelines",
        "custom_fields": {"salary": 1200000, "remote": True},
    }
    r = client.post(f"{API}/jobs", json=body)
    assert r.status_code == 201 and r.json()["custom_fields"]["remote"] is True