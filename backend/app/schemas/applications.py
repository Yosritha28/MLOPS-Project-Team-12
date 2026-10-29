from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.config import KEY_PATTERN
from app.schemas.inference import MatchResult


class ApplyRequest(BaseModel):
    resume_id: int


class AnalysisRequest(BaseModel):
    resume_id: int
    job_id: int


class StatusChange(BaseModel):
    status_key: str = Field(pattern=KEY_PATTERN, description="A key from /config/statuses")
    reason: str | None = Field(
        default=None,
        description="Optional note, stored with the decision as training feedback",
    )


class ApplicationOut(BaseModel):
    id: int
    job_id: int
    candidate_id: int
    resume_id: int
    status_key: str
    status_reason: str | None = None
    match_score: float = Field(ge=0, le=100)
    applied_at: datetime
    updated_at: datetime


class MyApplicationOut(ApplicationOut):
    job_title: str
    match: MatchResult


class ApplicationDetail(ApplicationOut):
    rank: int | None = Field(default=None, ge=1)
    candidate_name: str
    resume_skills: list[str]
    total_experience_years: float
    match: MatchResult


class ComparisonOut(BaseModel):
    job_id: int
    candidates: list[ApplicationDetail]