from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.responses import CONFLICT, FORBIDDEN, NOT_FOUND, UNAUTHORIZED
from app.core.samples import sample_application, sample_detail, sample_my_application
from app.core.security import bearer_scheme
from app.core.stub import mark_stub
from app.schemas.applications import (
    ApplicationDetail,
    ApplicationOut,
    ApplyRequest,
    ComparisonOut,
    MyApplicationOut,
    StatusChange,
)
from app.schemas.common import Page

router = APIRouter(
    tags=["applications"],
    dependencies=[Depends(mark_stub), Depends(bearer_scheme)],
    responses={**UNAUTHORIZED, **FORBIDDEN},
)


@router.post(
    "/jobs/{job_id}/apply",
    response_model=ApplicationOut,
    status_code=201,
    summary="Apply to a job with one of my resumes (candidate)",
    responses={**NOT_FOUND, **CONFLICT},
)
def apply(job_id: int, body: ApplyRequest) -> ApplicationOut:
    return sample_application(job_id=job_id, resume_id=body.resume_id)


@router.get(
    "/applications/mine",
    response_model=Page[MyApplicationOut],
    summary="My applications (candidate)",
)
def my_applications(
    status: str | None = Query(None, description="Filter by a status key from /config/statuses"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> Page[MyApplicationOut]:
    return Page[MyApplicationOut](
        items=[sample_my_application()], total=1, page=page, page_size=page_size
    )


@router.get(
    "/jobs/{job_id}/applications",
    response_model=Page[ApplicationDetail],
    summary="Applicants for my job, best match first (recruiter)",
    responses=NOT_FOUND,
)
def job_applications(
    job_id: int,
    status: str | None = Query(None, description="Filter by a status key from /config/statuses"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> Page[ApplicationDetail]:
    return Page[ApplicationDetail](
        items=[sample_detail(1, rank=1), sample_detail(2, rank=2)],
        total=2,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/jobs/{job_id}/compare",
    response_model=ComparisonOut,
    summary="Compare 2 to 5 applicants side by side (recruiter)",
    responses=NOT_FOUND,
)
def compare(
    job_id: int,
    ids: Annotated[
        list[int],
        Query(min_length=2, max_length=5, description="Application ids; repeat the parameter: ?ids=1&ids=2"),
    ],
) -> ComparisonOut:
    return ComparisonOut(
        job_id=job_id,
        candidates=[sample_detail(i, rank=n) for n, i in enumerate(ids, start=1)],
    )


@router.patch(
    "/applications/{application_id}/status",
    response_model=ApplicationOut,
    summary="Shortlist, reject or otherwise update an application (recruiter)",
    responses=NOT_FOUND,
)
def change_status(application_id: int, body: StatusChange) -> ApplicationOut:
    return sample_application(application_id).model_copy(
        update={"status_key": body.status_key, "status_reason": body.reason}
    )