from fastapi import APIRouter, Depends, Query, UploadFile

from app.core.responses import FORBIDDEN, NOT_FOUND, UNAUTHORIZED
from app.core.samples import sample_resume
from app.core.security import bearer_scheme
from app.core.stub import mark_stub
from app.schemas.common import ErrorResponse, Page
from app.schemas.resumes import ResumeOut

router = APIRouter(
    prefix="/resumes",
    tags=["resumes"],
    dependencies=[Depends(mark_stub), Depends(bearer_scheme)],
    responses={**UNAUTHORIZED, **FORBIDDEN},
)

UPLOAD_ERRORS = {
    413: {"model": ErrorResponse, "description": "File too large"},
    415: {"model": ErrorResponse, "description": "Only PDF or DOCX is accepted"},
}


@router.post(
    "",
    response_model=ResumeOut,
    status_code=201,
    summary="Upload a PDF or DOCX resume (candidate)",
    responses=UPLOAD_ERRORS,
)
def upload_resume(file: UploadFile) -> ResumeOut:
    resume = sample_resume()
    return resume.model_copy(
        update={
            "filename": file.filename or "resume",
            "content_type": file.content_type or "application/octet-stream",
            "size_bytes": file.size or 0,
        }
    )


@router.get("", response_model=Page[ResumeOut], summary="My resumes (candidate)")
def list_resumes(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)) -> Page[ResumeOut]:
    return Page[ResumeOut](items=[sample_resume()], total=1, page=page, page_size=page_size)


@router.get("/{resume_id}", response_model=ResumeOut, summary="One of my resumes", responses=NOT_FOUND)
def get_resume(resume_id: int) -> ResumeOut:
    return sample_resume(resume_id)


@router.delete("/{resume_id}", status_code=204, summary="Delete one of my resumes", responses=NOT_FOUND)
def delete_resume(resume_id: int) -> None:
    return None