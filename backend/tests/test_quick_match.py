import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.inference import MatchResult

client = TestClient(app)
API = "/api/v1"

RESUME = (
    "Data engineer with 4 years of experience. Built ETL pipelines with Python, SQL, Airflow and "
    "Spark on AWS. Deployed services with Docker and Kubernetes. B.Tech in Computer Science."
)
JOB = (
    "We need a data engineer. Required: Python, SQL, Airflow, Docker. "
    "Preferred: Kubernetes, Kafka. Minimum 3 years of experience."
)


@pytest.fixture(autouse=True)
def no_sbert(monkeypatch):
    monkeypatch.delenv("RESUMEIQ_SBERT", raising=False)


def test_quick_match_returns_a_real_result():
    r = client.post(f"{API}/analysis/quick-match", json={"resume_text": RESUME, "job_title": "Data Engineer", "job_text": JOB})
    assert r.status_code == 200
    assert "x-stub" not in r.headers
    body = r.json()
    MatchResult.model_validate(body)
    assert "python" in body["matched_skills"] and body["missing_skills"] == []


def test_quick_match_validates_input():
    r = client.post(f"{API}/analysis/quick-match", json={"resume_text": "short", "job_title": "x", "job_text": "short"})
    assert r.status_code == 422


def test_quick_match_file_accepts_txt():
    r = client.post(
        f"{API}/analysis/quick-match-file",
        files={"resume_file": ("cv.txt", RESUME.encode(), "text/plain")},
        data={"job_title": "Data Engineer", "job_text": JOB},
    )
    assert r.status_code == 200 and r.json()["overall_score"] > 0


def test_quick_match_file_rejects_unknown_type():
    r = client.post(
        f"{API}/analysis/quick-match-file",
        files={"resume_file": ("cv.exe", b"x" * 50, "application/octet-stream")},
        data={"job_title": "Data Engineer", "job_text": JOB},
    )
    assert r.status_code == 415


def test_demo_page_and_redirect():
    page = client.get("/demo")
    assert page.status_code == 200 and "ResumeIQ" in page.text
    assert page.headers["content-type"].startswith("text/html")
    assert client.get("/", follow_redirects=False).status_code in (302, 307)