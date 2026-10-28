from fastapi import APIRouter, Depends

from app.core.responses import CONFLICT, FORBIDDEN, NOT_FOUND, UNAUTHORIZED
from app.core.samples import STUB_TIME
from app.core.security import bearer_scheme
from app.core.stub import mark_stub
from app.schemas.config import (
    FeedbackSignal,
    FieldType,
    JobFieldCreate,
    JobFieldOut,
    JobFieldUpdate,
    ReloadResponse,
    ScoringOut,
    ScoringUpdate,
    SkillCreate,
    SkillOut,
    SkillUpdate,
    StatusCreate,
    StatusOut,
    StatusUpdate,
    Weights,
)

ADMIN_ONLY = {**UNAUTHORIZED, **FORBIDDEN}

router = APIRouter(
    prefix="/admin/config",
    tags=["admin: config"],
    dependencies=[Depends(mark_stub), Depends(bearer_scheme)],
    responses=ADMIN_ONLY,
)


# Config rows are never hard-deleted: set is_active to false instead.


@router.post("/skills", response_model=SkillOut, status_code=201, summary="Add a skill", responses=CONFLICT)
def create_skill(body: SkillCreate) -> SkillOut:
    return SkillOut(id=1, is_active=True, **body.model_dump())


@router.patch("/skills/{skill_id}", response_model=SkillOut, summary="Edit or deactivate a skill", responses=NOT_FOUND)
def update_skill(skill_id: int, body: SkillUpdate) -> SkillOut:
    return SkillOut(
        id=skill_id,
        name=body.name or "python",
        aliases=body.aliases or [],
        category=body.category,
        is_active=True if body.is_active is None else body.is_active,
    )


@router.post("/job-fields", response_model=JobFieldOut, status_code=201, summary="Add a job field", responses=CONFLICT)
def create_job_field(body: JobFieldCreate) -> JobFieldOut:
    return JobFieldOut(id=1, is_active=True, **body.model_dump())


@router.patch("/job-fields/{field_id}", response_model=JobFieldOut, summary="Edit or deactivate a job field", responses=NOT_FOUND)
def update_job_field(field_id: int, body: JobFieldUpdate) -> JobFieldOut:
    return JobFieldOut(
        id=field_id,
        key="salary",
        label=body.label or "Salary",
        type=FieldType.number,
        options=body.options or [],
        required=bool(body.required),
        order=body.order or 0,
        is_active=True if body.is_active is None else body.is_active,
    )


@router.post("/statuses", response_model=StatusOut, status_code=201, summary="Add an application status", responses=CONFLICT)
def create_status(body: StatusCreate) -> StatusOut:
    return StatusOut(id=1, is_active=True, **body.model_dump())


@router.patch("/statuses/{status_id}", response_model=StatusOut, summary="Edit or deactivate a status", responses=NOT_FOUND)
def update_status(status_id: int, body: StatusUpdate) -> StatusOut:
    return StatusOut(
        id=status_id,
        key="interview",
        label=body.label or "Interview",
        order=body.order or 0,
        feedback=body.feedback or FeedbackSignal.neutral,
        is_active=True if body.is_active is None else body.is_active,
    )


@router.patch("/scoring", response_model=ScoringOut, summary="Change scoring weights or the active model version")
def update_scoring(body: ScoringUpdate) -> ScoringOut:
    return ScoringOut(
        weights=body.weights or Weights(tfidf=0.3, sbert=0.5, skills=0.2),
        model_version=body.model_version or "hybrid-v1",
        updated_at=STUB_TIME,
        updated_by=1,
    )


@router.post("/reload", response_model=ReloadResponse, summary="Make the AI use the latest config without a redeploy")
def reload_config() -> ReloadResponse:
    return ReloadResponse(reloaded=True, at=STUB_TIME)