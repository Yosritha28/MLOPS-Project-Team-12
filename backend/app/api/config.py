from fastapi import APIRouter, Depends

from app.core.responses import UNAUTHORIZED
from app.core.samples import STUB_TIME
from app.core.security import bearer_scheme
from app.core.stub import mark_stub
from app.schemas.config import (
    FeedbackSignal,
    FieldType,
    JobFieldOut,
    ScoringOut,
    SkillOut,
    StatusOut,
    Weights,
)

router = APIRouter(
    prefix="/config",
    tags=["config"],
    dependencies=[Depends(mark_stub), Depends(bearer_scheme)],
    responses=UNAUTHORIZED,
)


@router.get("/skills", response_model=list[SkillOut], summary="Active skills (the skill list is data, not code)")
def list_skills() -> list[SkillOut]:
    return [SkillOut(id=1, name="python", aliases=["py"], category="programming", is_active=True)]


@router.get("/job-fields", response_model=list[JobFieldOut], summary="Extra fields the job form should show")
def list_job_fields() -> list[JobFieldOut]:
    return [
        JobFieldOut(id=1, key="salary", label="Salary (INR per year)", type=FieldType.number, options=[], required=False, order=1, is_active=True),
        JobFieldOut(id=2, key="remote", label="Remote allowed", type=FieldType.boolean, options=[], required=False, order=2, is_active=True),
    ]


@router.get("/statuses", response_model=list[StatusOut], summary="Application statuses, in display order")
def list_statuses() -> list[StatusOut]:
    return [
        StatusOut(id=1, key="applied", label="Applied", order=1, feedback=FeedbackSignal.neutral, is_active=True),
        StatusOut(id=2, key="shortlisted", label="Shortlisted", order=2, feedback=FeedbackSignal.positive, is_active=True),
        StatusOut(id=3, key="rejected", label="Rejected", order=3, feedback=FeedbackSignal.negative, is_active=True),
    ]


@router.get("/scoring", response_model=ScoringOut, summary="Current scoring weights and active model version")
def get_scoring() -> ScoringOut:
    return ScoringOut(
        weights=Weights(tfidf=0.3, sbert=0.5, skills=0.2),
        model_version="hybrid-v1",
        updated_at=STUB_TIME,
        updated_by=None,
    )