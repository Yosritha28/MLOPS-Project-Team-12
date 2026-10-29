from fastapi import APIRouter, Depends

from app.core.responses import FORBIDDEN, NOT_FOUND, UNAUTHORIZED
from app.core.samples import sample_match
from app.core.security import bearer_scheme
from app.core.stub import mark_stub
from app.schemas.applications import AnalysisRequest
from app.schemas.inference import MatchResult

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
    dependencies=[Depends(mark_stub), Depends(bearer_scheme)],
    responses={**UNAUTHORIZED, **FORBIDDEN},
)


@router.post(
    "/match",
    response_model=MatchResult,
    summary="Match one of my resumes against a job (nothing is saved)",
    responses=NOT_FOUND,
)
def match(body: AnalysisRequest) -> MatchResult:
    return sample_match()