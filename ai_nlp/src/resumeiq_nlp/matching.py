"""Hybrid matching: TF-IDF + SBERT (optional) + skill overlap. Weights are an input, not a constant."""
import os
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .extract import SCHEMA_VERSION, parse_job_text, parse_resume_text

DEFAULT_WEIGHTS = {"tfidf": 0.3, "sbert": 0.5, "skills": 0.2}
SBERT_MODEL_NAME = "all-MiniLM-L6-v2"

_sbert_model = None
_sbert_failed = False


def sbert_requested(flag: bool | None = None) -> bool:
    return flag if flag is not None else os.getenv("RESUMEIQ_SBERT", "0") == "1"


def _get_sbert():
    global _sbert_model, _sbert_failed
    if _sbert_model is None and not _sbert_failed:
        try:
            from sentence_transformers import SentenceTransformer

            _sbert_model = SentenceTransformer(SBERT_MODEL_NAME)
        except Exception:
            _sbert_failed = True
    return _sbert_model


def tfidf_similarity(a: str, b: str, corpus: list[str] | None = None) -> float:
    if not a.strip() or not b.strip():
        return 0.0
    try:
        vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
        vec.fit(list(corpus) if corpus else [a, b])
        m = vec.transform([a, b])
        return float(cosine_similarity(m[0], m[1])[0, 0])
    except ValueError:  # empty vocabulary
        return 0.0


def sbert_similarity(a: str, b: str) -> float | None:
    model = _get_sbert()
    if model is None:
        return None
    emb = model.encode([a[:4000], b[:4000]], normalize_embeddings=True)
    return max(0.0, min(1.0, float(emb[0] @ emb[1])))


def skills_score(resume_skills: list[str], required: list[str], preferred: list[str]) -> float:
    have = {s.lower() for s in resume_skills}
    req = sum(1 for s in required if s.lower() in have) / len(required) if required else None
    pref = sum(1 for s in preferred if s.lower() in have) / len(preferred) if preferred else None
    if req is not None and pref is not None:
        return 0.8 * req + 0.2 * pref
    if req is not None:
        return req
    return pref if pref is not None else 0.0


def score_components(resume_text, job_title, job_text, use_sbert=None, corpus=None, skills=None) -> dict:
    """The three raw scores (each 0..1) plus the parsed resume and job. sbert is None when not used."""
    resume = parse_resume_text(resume_text, skills)
    job = parse_job_text(job_title, job_text, skills)
    job_full = f"{job_title}\n{job_text}"
    sbert = sbert_similarity(resume_text, job_full) if sbert_requested(use_sbert) else None
    return {
        "tfidf": tfidf_similarity(resume_text, job_full, corpus),
        "sbert": sbert,
        "skills": skills_score(resume["skills"], job["required_skills"], job["preferred_skills"]),
        "resume": resume,
        "job": job,
    }


def _check_weights(w: dict) -> None:
    if set(w) != {"tfidf", "sbert", "skills"} or any(v < 0 for v in w.values()):
        raise ValueError("weights must have the keys tfidf, sbert, skills and no negative values")
    if abs(sum(w.values()) - 1) > 0.001:
        raise ValueError("weights must sum to 1")


def _label(score: float) -> str:
    return "Strong" if score >= 75 else "Moderate" if score >= 50 else "Weak"


def match_texts(resume_text, job_title, job_text, weights=None, skills=None, use_sbert=None) -> dict:
    """Return a MatchResult (inference contract v1.1) for a resume and a job description."""
    t0 = time.perf_counter()
    w = dict(weights or DEFAULT_WEIGHTS)
    _check_weights(w)
    c = score_components(resume_text, job_title, job_text, use_sbert=use_sbert, skills=skills)
    resume, job = c["resume"], c["job"]
    warnings = list(resume["warnings"])

    sbert_on = c["sbert"] is not None
    if not sbert_on:
        if sbert_requested(use_sbert):
            warnings.append("SBERT is not available, so its weight was shared by the other scores.")
        rest = w["tfidf"] + w["skills"]
        w = {"tfidf": 0.5, "sbert": 0.0, "skills": 0.5} if rest <= 0 else {
            "tfidf": w["tfidf"] / rest, "sbert": 0.0, "skills": w["skills"] / rest}
    w = {k: round(v, 4) for k, v in w.items()}
    comp = {"tfidf": round(c["tfidf"], 4), "sbert": round(c["sbert"] or 0.0, 4), "skills": round(c["skills"], 4)}
    overall = max(0.0, min(100.0, 100 * sum(w[k] * comp[k] for k in w)))

    wanted = [*job["required_skills"], *job["preferred_skills"]]
    have = {s.lower() for s in resume["skills"]}
    matched = [s for s in wanted if s.lower() in have]
    missing = [s for s in job["required_skills"] if s.lower() not in have]
    if not wanted:
        warnings.append("No known skills were found in the job description, so the skills score is 0.")

    years, min_years = resume["total_experience_years"], job["min_experience_years"]
    strengths, gaps = [], []
    if job["required_skills"]:
        got = len(job["required_skills"]) - len(missing)
        strengths.append(f"Covers {got} of {len(job['required_skills'])} required skills")
    if min_years > 0 and years >= min_years:
        strengths.append(f"{years:g} years of experience meets the {min_years:g}-year requirement")
    if comp["tfidf"] >= 0.35:
        strengths.append("Resume wording closely follows the job description")
    if missing:
        gaps.append("Missing required skills: " + ", ".join(missing))
    if min_years > 0 and years < min_years:
        gaps.append(f"Experience ({years:g} years) is below the {min_years:g}-year requirement")
    if missing:
        detail = "Missing: " + ", ".join(missing[:5]) + "."
    elif job["required_skills"]:
        detail = "All required skills are covered."
    else:
        detail = "The job lists no recognised required skills."

    return {
        "schema_version": SCHEMA_VERSION,
        "overall_score": round(overall, 1),
        "component_scores": comp,
        "weights": w,
        "matched_skills": matched,
        "missing_skills": missing,
        "explanation": {"summary": f"{_label(overall)} match ({overall:.0f}/100). {detail}", "strengths": strengths, "gaps": gaps},
        "model_version": "hybrid-v1" if sbert_on else "tfidf-skills-v1",
        "latency_ms": round((time.perf_counter() - t0) * 1000, 1),
        "warnings": warnings,
        "extras": {
            "resume_skills": resume["skills"],
            "job_required_skills": job["required_skills"],
            "job_preferred_skills": job["preferred_skills"],
            "resume_experience_years": years,
            "job_min_experience_years": min_years,
        },
    }