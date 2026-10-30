from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, UploadFile
from resumeiq_nlp import extract_text, match_texts

from app.schemas.common import ErrorResponse
from app.schemas.inference import MatchResult
from app.schemas.quick import QuickMatchRequest

# Real (not stub) endpoints. They need no login yet: for demos and prototyping until auth is built.
router = APIRouter(prefix="/analysis", tags=["analysis"])

MAX_BYTES = 5 * 1024 * 1024
FILE_ERRORS = {
    413: {"model": ErrorResponse, "description": "File larger than 5 MB"},
    415: {"model": ErrorResponse, "description": "Only PDF, DOCX or TXT is accepted"},
    422: {"model": ErrorResponse, "description": "No readable text in the file"},
}


@router.post(
    "/quick-match",
    response_model=MatchResult,
    summary="Match pasted resume text against a job description (real AI result)",
)
def quick_match(body: QuickMatchRequest) -> MatchResult:
    return MatchResult.model_validate(match_texts(body.resume_text, body.job_title, body.job_text))


@router.post(
    "/quick-match-file",
    response_model=MatchResult,
    summary="Match an uploaded resume (PDF, DOCX or TXT) against a job description",
    responses=FILE_ERRORS,
)
def quick_match_file(
    resume_file: UploadFile,
    job_title: Annotated[str, Form(min_length=1)],
    job_text: Annotated[str, Form(min_length=20)],
) -> MatchResult:
    data = resume_file.file.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="File too large (max 5 MB).")
    try:
        text = extract_text(data, resume_file.filename or "")
    except ValueError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=422, detail="Could not read this file.") from exc
    if len(text.strip()) < 20:
        raise HTTPException(status_code=422, detail="No readable text found in the file (is it a scanned image?).")
    return MatchResult.model_validate(match_texts(text, job_title, job_text))