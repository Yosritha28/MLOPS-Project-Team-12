
"""Hybrid resume-to-job matching for ResumeIQ.

Scores are normalized to [0, 1]. The final overall_score is on a 0–100 scale.
Sentence-BERT is loaded lazily so importing this package does not download a model.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from typing import Callable, Sequence

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SCHEMA_VERSION = "1.1"
MODEL_VERSION = "hybrid-v1"
DEFAULT_WEIGHTS = {"tfidf": 0.3, "sbert": 0.5, "skills": 0.2}

# A starter vocabulary. Extend it as your evaluation dataset grows.
KNOWN_SKILLS = {
    "python", "java", "javascript", "typescript", "c++", "c#", "sql",
    "mysql", "postgresql", "mongodb", "fastapi", "flask", "django",
    "react", "node.js", "html", "css", "git", "github", "docker",
    "kubernetes", "aws", "azure", "gcp", "linux", "rest api", "api",
    "machine learning", "deep learning", "nlp", "natural language processing",
    "pytorch", "tensorflow", "scikit-learn", "pandas", "numpy",
    "data analysis", "data engineering", "mlflow", "dvc", "ci/cd",
    "communication", "leadership", "project management", "agile",
    "sentence-transformers", "transformers", "statistics",
}


@dataclass
class MatchingConfig:
    """Configurable model settings."""

    weights: dict[str, float] | None = None
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    model_version: str = MODEL_VERSION


def _normalize_text(text: str) -> str:
    """Normalize whitespace and reject empty/non-string input."""
    if not isinstance(text, str):
        raise TypeError("Resume and job text must be strings.")
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        raise ValueError("Resume and job text must not be empty.")
    return text


def _validate_weights(weights: dict[str, float] | None) -> dict[str, float]:
    values = dict(DEFAULT_WEIGHTS if weights is None else weights)
    expected = set(DEFAULT_WEIGHTS)

    if set(values) != expected:
        raise ValueError("Weights must contain exactly: tfidf, sbert, skills.")

    for name, value in values.items():
        if not isinstance(value, (int, float)) or not 0 <= value <= 1:
            raise ValueError(f"Weight '{name}' must be between 0 and 1.")

    if not np.isclose(sum(values.values()), 1.0, atol=1e-6):
        raise ValueError("Weights must sum to 1.0.")

    return {name: float(value) for name, value in values.items()}


def _extract_skills(text: str) -> set[str]:
    """Find known skills in text using case-insensitive phrase matching."""
    normalized = text.lower()
    found: set[str] = set()

    for skill in KNOWN_SKILLS:
        pattern = r"(?<![a-z0-9+#.])" + re.escape(skill.lower()) + r"(?![a-z0-9+#.])"
        if re.search(pattern, normalized):
            found.add(skill)

    return found


def _tfidf_score(resume_text: str, job_text: str) -> float:
    """Compute cosine similarity between TF-IDF vectors."""
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    try:
        vectors = vectorizer.fit_transform([resume_text, job_text])
        score = float(cosine_similarity(vectors[0], vectors[1])[0, 0])
    except ValueError:
        # For example, both texts contain only stop words.
        score = 0.0
    return float(np.clip(score, 0.0, 1.0))


def _sbert_score(
    resume_text: str,
    job_text: str,
    model_name: str,
    embedder: Callable[[Sequence[str]], object] | None = None,
) -> tuple[float, str | None]:
    """Compute Sentence-BERT cosine similarity.

    An embedder can be injected in tests. If model loading fails, return a
    zero score and a warning rather than silently presenting TF-IDF as SBERT.
    """
    try:
        if embedder is None:
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer(model_name)
            embedder = model.encode

        embeddings = np.asarray(
            embedder([resume_text, job_text]), dtype=float
        )

        if embeddings.ndim != 2 or embeddings.shape[0] != 2:
            raise ValueError("Embedder must return two embedding vectors.")

        first, second = embeddings[0], embeddings[1]
        denominator = float(np.linalg.norm(first) * np.linalg.norm(second))

        if denominator == 0:
            return 0.0, "Sentence-BERT returned a zero-length embedding."

        cosine = float(np.dot(first, second) / denominator)

        # Cosine similarity is [-1, 1]; map it to [0, 1].
        score = (cosine + 1.0) / 2.0
        return float(np.clip(score, 0.0, 1.0)), None

    except Exception as exc:
        return 0.0, (
            "Sentence-BERT was unavailable; its score is 0 for this result. "
            f"Details: {type(exc).__name__}."
        )


def match_resume_to_job(
    resume_text: str,
    job_text: str,
    required_skills: Sequence[str] | None = None,
    preferred_skills: Sequence[str] | None = None,
    weights: dict[str, float] | None = None,
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    model_version: str = MODEL_VERSION,
    embedder: Callable[[Sequence[str]], object] | None = None,
) -> dict:
    """Return a ResumeIQ inference result conforming to contract v1.1."""
    started = time.perf_counter()

    resume = _normalize_text(resume_text)
    job = _normalize_text(job_text)
    selected_weights = _validate_weights(weights)

    resume_skills = _extract_skills(resume)

    # Explicit skills from structured parsing take priority as job requirements.
    required = {
        str(skill).strip().lower()
        for skill in (required_skills or [])
        if str(skill).strip()
    }
    preferred = {
        str(skill).strip().lower()
        for skill in (preferred_skills or [])
        if str(skill).strip()
    }

    # If structured job skills were not supplied, infer them from the description.
    if not required and not preferred:
        required = _extract_skills(job)

    target_skills = required | preferred
    matched = sorted(resume_skills & target_skills)
    missing = sorted(target_skills - resume_skills)

    # Required skills count more strongly than preferred skills.
    if required or preferred:
        skill_points = len(resume_skills & required) + (
            0.5 * len(resume_skills & preferred)
        )
        possible_points = len(required) + (0.5 * len(preferred))
        skill_score = skill_points / possible_points if possible_points else 0.0
    else:
        skill_score = 0.0

    tfidf_score = _tfidf_score(resume, job)
    sbert_score, sbert_warning = _sbert_score(
        resume, job, model_name, embedder=embedder
    )

    component_scores = {
        "tfidf": round(tfidf_score, 4),
        "sbert": round(sbert_score, 4),
        "skills": round(float(np.clip(skill_score, 0, 1)), 4),
    }

    overall = 100 * sum(
        selected_weights[name] * component_scores[name]
        for name in selected_weights
    )

    warnings: list[str] = []
    if sbert_warning:
        warnings.append(sbert_warning)
    if not target_skills:
        warnings.append(
            "No known job skills were identified; the skills score is 0."
        )

    if matched:
        strengths = [f"Matching skills: {', '.join(matched)}."]
    else:
        strengths = ["No direct skill matches were identified from the available skill vocabulary."]

    if missing:
        gaps = [f"Skills to develop or verify: {', '.join(missing)}."]
    else:
        gaps = ["No missing skills were identified from the available skill vocabulary."]

    summary = (
        f"Hybrid match score: {overall:.1f}%. "
        f"Text similarity and skill overlap are combined using the configured weights."
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "overall_score": round(float(np.clip(overall, 0, 100)), 2),
        "component_scores": component_scores,
        "weights": selected_weights,
        "matched_skills": matched,
        "missing_skills": missing,
        "explanation": {
            "summary": summary,
            "strengths": strengths,
            "gaps": gaps,
        },
        "model_version": model_version,
        "latency_ms": round((time.perf_counter() - started) * 1000, 2),
        "warnings": warnings,
    }
