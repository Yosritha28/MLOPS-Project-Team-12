"""Rule-based extraction: skills, experience years, education. The skill list is data, not code."""
import json
import re
from functools import lru_cache
from pathlib import Path

SCHEMA_VERSION = "1.1"
DATA_DIR = Path(__file__).parent / "data"

_EDU_WORDS = ("b.tech", "btech", "m.tech", "degree", "bachelor", "master", "university", "college", "diploma", "b.sc", "m.sc")
_YEARS = re.compile(r"(\d{1,2}(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)\b", re.I)
_LEVELS = [
    ("PhD", re.compile(r"\b(?:ph\.?d|doctorate)\b", re.I)),
    ("Master", re.compile(r"\b(?:master'?s?|m\.?\s?tech|m\.?\s?sc|mba)\b", re.I)),
    ("Bachelor", re.compile(r"\b(?:bachelor'?s?|b\.?\s?tech|b\.?\s?sc|bca)\b", re.I)),
    ("Diploma", re.compile(r"\bdiploma\b", re.I)),
]
_PREFERRED_MARKERS = ("preferred", "nice to have", "good to have", "bonus")


@lru_cache(maxsize=1)
def default_skills() -> list[dict]:
    """The built-in skill list (name, aliases, category). The backend can pass its own list instead."""
    return json.loads((DATA_DIR / "skills_default.json").read_text(encoding="utf-8"))


def _term_pattern(term: str) -> re.Pattern:
    # Not preceded by a letter, digit, + # or "." and not followed by a letter, digit, + or #:
    # "java" does not match "javascript", "sql" not "mysql", and "js" not the end of "node.js".
    return re.compile(r"(?<![a-z0-9+#.])" + re.escape(term.lower()) + r"(?![a-z0-9+#])")


def extract_skills(text: str, skills: list[dict] | None = None) -> list[str]:
    """Skill names found in the text, in order of first appearance."""
    low = text.lower()
    found: list[tuple[int, str]] = []
    for skill in skills if skills is not None else default_skills():
        if skill.get("is_active", True) is False:
            continue
        positions = []
        for term in [skill["name"], *skill.get("aliases", [])]:
            m = _term_pattern(term).search(low)
            if m:
                positions.append(m.start())
        if positions:
            found.append((min(positions), skill["name"]))
    return [name for _, name in sorted(found)]


def extract_experience_years(text: str) -> float:
    """Largest 'N years' mention that is not about education."""
    values = []
    for m in _YEARS.finditer(text):
        context = text[max(0, m.start() - 40): m.end() + 40].lower()
        if any(word in context for word in _EDU_WORDS):
            continue
        values.append(float(m.group(1)))
    return min(max(values), 40.0) if values else 0.0


def extract_education_levels(text: str) -> list[str]:
    return [name for name, pattern in _LEVELS if pattern.search(text)]


def parse_resume_text(text: str, skills: list[dict] | None = None) -> dict:
    found = extract_skills(text, skills)
    warnings = []
    if len(text.strip()) < 200:
        warnings.append("Very little text found; the resume may be a scan or too short.")
    if not found:
        warnings.append("No known skills were detected in the resume.")
    return {
        "schema_version": SCHEMA_VERSION,
        "raw_text": text,
        "skills": found,
        "education": [{"degree": level} for level in extract_education_levels(text)],
        "experience": [],
        "projects": [],
        "total_experience_years": extract_experience_years(text),
        "warnings": warnings,
    }


def parse_job_text(title: str, text: str, skills: list[dict] | None = None) -> dict:
    low = text.lower()
    cut = [low.find(m) for m in _PREFERRED_MARKERS if m in low]
    split_at = min(cut) if cut else len(text)
    required = extract_skills(text[:split_at], skills)
    preferred = [s for s in extract_skills(text[split_at:], skills) if s not in required]
    levels = extract_education_levels(text)
    return {
        "schema_version": SCHEMA_VERSION,
        "title": title,
        "raw_text": text,
        "required_skills": required,
        "preferred_skills": preferred,
        "min_experience_years": extract_experience_years(text),
        "education_level": levels[0] if levels else None,
    }