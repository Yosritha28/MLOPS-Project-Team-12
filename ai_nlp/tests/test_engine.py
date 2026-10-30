import io
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from resumeiq_nlp import (
    extract_experience_years,
    extract_skills,
    match_texts,
    parse_job_text,
    parse_resume_text,
)
from resumeiq_nlp.readers import extract_text

CONTRACTS = Path(__file__).resolve().parents[2] / "contracts"

GOOD_RESUME = (
    "Data engineer with 4 years of experience. Built ETL pipelines with Python, SQL, Airflow and "
    "Spark on AWS. Deployed services with Docker and Kubernetes. B.Tech in Computer Science."
)
BAD_RESUME = (
    "Marketing executive with 5 years of experience in SEO, content marketing and social media "
    "marketing. Managed Google Analytics reports."
)
JOB = (
    "We need a data engineer. Required: Python, SQL, Airflow, Docker. "
    "Preferred: Kubernetes, Kafka. Minimum 3 years of experience."
)


def validator(def_name):
    schema = json.loads((CONTRACTS / "inference_schema.json").read_text(encoding="utf-8"))
    return Draft202012Validator({"$ref": f"#/$defs/{def_name}", "$defs": schema["$defs"]})


def test_skill_extraction_handles_aliases_and_special_names():
    found = extract_skills("Worked with Python, C++, C#, Node.js, Postgres and Docker.")
    assert set(found) == {"python", "c++", "c#", "node.js", "postgresql", "docker"}
    assert extract_skills("javascript") == ["javascript"]  # not 'java'
    assert extract_skills("mysql") == ["mysql"]  # not 'sql'


def test_custom_skill_list_is_used():
    custom = [{"name": "cobol", "aliases": ["mainframe cobol"], "category": "legacy"}]
    assert extract_skills("Ten years of mainframe COBOL", custom) == ["cobol"]


def test_experience_years():
    assert extract_experience_years("4 years of experience in data") == 4
    assert extract_experience_years("5+ years as a developer") == 5
    assert extract_experience_years("B.Tech 2020-2024 (4 years)") == 0
    assert extract_experience_years("nothing here") == 0


def test_job_parsing_splits_required_and_preferred():
    job = parse_job_text("Data Engineer", JOB)
    assert set(job["required_skills"]) == {"python", "sql", "airflow", "docker"}
    assert set(job["preferred_skills"]) == {"kubernetes", "kafka"}
    assert job["min_experience_years"] == 3


def test_better_resume_scores_higher_and_gaps_are_reported():
    good = match_texts(GOOD_RESUME, "Data Engineer", JOB, use_sbert=False)
    bad = match_texts(BAD_RESUME, "Data Engineer", JOB, use_sbert=False)
    assert 0 <= bad["overall_score"] < good["overall_score"] <= 100
    assert good["missing_skills"] == [] and "python" in good["matched_skills"]
    assert "python" in bad["missing_skills"]


def test_weights_are_renormalised_when_sbert_is_off():
    r = match_texts(GOOD_RESUME, "Data Engineer", JOB, use_sbert=False)
    assert r["weights"]["sbert"] == 0 and r["component_scores"]["sbert"] == 0
    assert abs(sum(r["weights"].values()) - 1) < 1e-6
    assert r["model_version"] == "tfidf-skills-v1"


def test_custom_weights_change_the_score():
    r = match_texts(GOOD_RESUME, "Data Engineer", JOB, weights={"tfidf": 0, "sbert": 0, "skills": 1}, use_sbert=False)
    assert r["component_scores"]["skills"] == pytest.approx(0.9, abs=1e-3)
    assert r["overall_score"] == pytest.approx(90.0, abs=0.2)


def test_bad_weights_are_rejected():
    with pytest.raises(ValueError):
        match_texts(GOOD_RESUME, "Data Engineer", JOB, weights={"tfidf": 0.9, "sbert": 0.9, "skills": 0.9})


def test_outputs_satisfy_the_inference_contract():
    validator("MatchResult").validate(match_texts(GOOD_RESUME, "Data Engineer", JOB, use_sbert=False))
    validator("ParsedResume").validate(parse_resume_text(GOOD_RESUME))
    validator("ParsedJob").validate(parse_job_text("Data Engineer", JOB))


def test_txt_and_unsupported_files():
    assert "python" in extract_text(b"I know Python", "cv.txt").lower()
    with pytest.raises(ValueError):
        extract_text(b"x", "cv.exe")


def test_docx_roundtrip():
    import docx

    d = docx.Document()
    d.add_paragraph("Skills: Python and SQL")
    buf = io.BytesIO()
    d.save(buf)
    assert "Python" in extract_text(buf.getvalue(), "cv.docx")


def test_pdf_roundtrip():
    import pymupdf

    doc = pymupdf.open()
    doc.new_page().insert_text((72, 72), "Skills: Python and SQL")
    data = doc.tobytes()
    doc.close()
    assert "Python" in extract_text(data, "cv.pdf")