from fastapi import APIRouter, Depends, Query

from app.core.responses import FORBIDDEN, NOT_FOUND, UNAUTHORIZED
from app.core.samples import sample_job, sample_match
from app.core.security import bearer_scheme
from app.core.stub import mark_stub
from app.schemas.common import Page
from app.schemas.jobs import JobCreate, JobOut, JobRecommendation, JobUpdate

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    dependencies=[Depends(mark_stub), Depends(bearer_scheme)],
    responses={**UNAUTHORIZED, **FORBIDDEN},
)


@router.get("", response_model=Page[JobOut], summary="Browse jobs (candidate and recruiter)")
def list_jobs(
    q: str | None = Query(None, description="Search in title and description"),
    only_open: bool = True,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> Page[JobOut]:
    return Page[JobOut](items=[sample_job()], total=1, page=page, page_size=page_size)


# NOTE: this route must stay ABOVE /{job_id}, otherwise "recommended" is read as an id.
@router.get(
    "/recommended",
    response_model=list[JobRecommendation],
    summary="Jobs that best match my latest resume (candidate)",
)
def recommended_jobs(limit: int = Query(10, ge=1, le=50)) -> list[JobRecommendation]:
    return [JobRecommendation(job=sample_job(), match=sample_match())]


@router.get("/{job_id}", response_model=JobOut, summary="One job", responses=NOT_FOUND)
def get_job(job_id: int) -> JobOut:
    return sample_job(job_id)


@router.post("", response_model=JobOut, status_code=201, summary="Create a job (recruiter)")
def create_job(body: JobCreate) -> JobOut:
    return sample_job().model_copy(update=body.model_dump())


@router.patch("/{job_id}", response_model=JobOut, summary="Edit or close my job (recruiter)", responses=NOT_FOUND)
def update_job(job_id: int, body: JobUpdate) -> JobOut:
    return sample_job(job_id).model_copy(update=body.model_dump(exclude_unset=True))


@router.delete("/{job_id}", status_code=204, summary="Delete my job (recruiter)", responses=NOT_FOUND)
def delete_job(job_id: int) -> None:
    return None