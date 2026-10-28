from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.inference import MatchResult


class JobBase(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    min_experience_years: float = Field(default=0, ge=0)
    education_level: str | None = None
    custom_fields: dict[str, Any] = Field(
        default_factory=dict,
        description="Values for the admin-defined job fields, keyed by field key (see /config/job-fields)",
    )


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None, min_length=1)
    required_skills: list[str] | None = None
    preferred_skills: list[str] | None = None
    min_experience_years: float | None = Field(default=None, ge=0)
    education_level: str | None = None
    custom_fields: dict[str, Any] | None = None
    is_open: bool | None = None


class JobOut(JobBase):
    id: int
    recruiter_id: int
    is_open: bool
    created_at: datetime
    updated_at: datetime


class JobRecommendation(BaseModel):
    job: JobOut
    match: MatchResult