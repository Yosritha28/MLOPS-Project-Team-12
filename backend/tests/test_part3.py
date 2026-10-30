from fastapi.testclient import TestClient

from app.main import app
from app.schemas.inference import MatchResult

client = TestClient(app)
API = "/api/v1"


def test_analysis_returns_the_inference_contract_shape():
    r = client.post(f"{API}/analysis/match", json={"resume_id": 1, "job_id": 1})
    assert r.status_code == 200
    MatchResult.model_validate(r.json())


def test_apply_creates_an_application():
    r = client.post(f"{API}/jobs/5/apply", json={"resume_id": 2})
    assert r.status_code == 201
    body = r.json()
    assert body["job_id"] == 5 and body["resume_id"] == 2 and body["status_key"] == "applied"


def test_compare_needs_two_to_five_ids():
    assert client.get(f"{API}/jobs/1/compare?ids=1").status_code == 422
    r = client.get(f"{API}/jobs/1/compare?ids=1&ids=2")
    assert r.status_code == 200 and len(r.json()["candidates"]) == 2


def test_status_change_validates_the_key_and_echoes_the_decision():
    bad = client.patch(f"{API}/applications/1/status", json={"status_key": "Not Valid!"})
    assert bad.status_code == 422
    ok = client.patch(
        f"{API}/applications/1/status",
        json={"status_key": "shortlisted", "reason": "strong match"},
    )
    assert ok.status_code == 200
    assert ok.json()["status_key"] == "shortlisted" and ok.json()["status_reason"] == "strong match"


def test_admin_can_list_and_update_users():
    assert client.get(f"{API}/admin/users?role=recruiter").status_code == 200
    r = client.patch(f"{API}/admin/users/3", json={"is_active": False})
    assert r.status_code == 200
    assert r.json()["id"] == 3 and r.json()["is_active"] is False


def test_metrics_is_prometheus_text():
    r = client.get("/metrics")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/plain")
    assert "resumeiq_up" in r.text