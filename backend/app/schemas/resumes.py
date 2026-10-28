from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ResumeStatus(str, Enum):
    parsed = "parsed"
    failed = "failed"


class ResumeOut(BaseModel):
    id: int
    candidate_id: int
    filename: str
    content_type: str
    size_bytes: int
    status: ResumeStatus
    skills: list[str]
    total_experience_years: float
    warnings: list[str]
    uploaded_at: datetime