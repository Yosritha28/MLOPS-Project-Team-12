
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from resumeiq_nlp.matching import match_resume_to_job


CONTRACTS = Path(__file__).resolve().parents[2] / "contracts"


def fake_embedder(texts):
    """Deterministic embeddings so tests don't download a model."""
    return [[1.0, 0.0], [0.8, 0.6]]


def test_matching_returns_contract_v11_result():
    result = match_resume_to_job(
        resume_text="Python SQL Docker FastAPI. Built data pipelines.",
        job_text="Python SQL Docker Kubernetes. Build data pipelines.",
        required_skills=["python", "sql", "docker", "kubernetes"],
        weights={"tfidf": 0.3, "sbert": 0.5, "skills": 0.2},
        embedder=fake_embedder,
    )

    schema = json.loads(
        (CONTRACTS / "inference_schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(
        {"$ref": "#/$defs/MatchResult", "$defs": schema["$defs"]}
    )
    validator.validate(result)

    assert result["schema_version"] == "1.1"
    assert 0 <= result["overall_score"] <= 100
    assert result["matched_skills"] == ["docker", "python", "sql"]
    assert result["missing_skills"] == ["kubernetes"]
    assert result["warnings"] == []


def test_weights_must_sum_to_one():
    with pytest.raises(ValueError, match="sum to 1.0"):
        match_resume_to_job(
            "Python developer",
            "Python engineer",
            weights={"tfidf": 0.5, "sbert": 0.5, "skills": 0.5},
            embedder=fake_embedder,
        )


def test_empty_resume_is_rejected():
    with pytest.raises(ValueError, match="must not be empty"):
        match_resume_to_job(
            "",
            "Python engineer",
            embedder=fake_embedder,
        )


def test_scores_are_bounded():
    result = match_resume_to_job(
        "Python SQL Docker",
        "Python SQL Docker",
        required_skills=["python", "sql"],
        embedder=fake_embedder,
    )

    assert 0 <= result["overall_score"] <= 100
    for score in result["component_scores"].values():
        assert 0 <= score <= 1


def test_result_includes_latency_and_model_version():
    result = match_resume_to_job(
        "Python developer",
        "Python engineer",
        embedder=fake_embedder,
    )

    assert result["latency_ms"] >= 0
    assert result["model_version"] == "hybrid-v1"
