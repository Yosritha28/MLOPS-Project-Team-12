from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.core.security import bearer_scheme
from app.core.stub import mark_stub
from app.schemas.auth import LoginRequest, RegisterRequest, Role, TokenResponse, UserOut
from app.schemas.common import ErrorResponse

router = APIRouter(prefix="/auth", tags=["auth"], dependencies=[Depends(mark_stub)])

_STUB_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


@router.post(
    "/register",
    response_model=UserOut,
    status_code=201,
    summary="Create a candidate or recruiter account",
    responses={409: {"model": ErrorResponse, "description": "Email already registered"}},
)
def register(body: RegisterRequest) -> UserOut:
    return UserOut(
        id=1,
        email=body.email,
        full_name=body.full_name,
        role=Role(body.role),
        is_active=True,
        created_at=_STUB_TIME,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Log in and receive a JWT",
    responses={401: {"model": ErrorResponse, "description": "Wrong email or password"}},
)
def login(body: LoginRequest) -> TokenResponse:
    return TokenResponse(access_token="stub-token", expires_in=3600)


@router.get(
    "/me",
    response_model=UserOut,
    summary="The logged-in user",
    dependencies=[Depends(bearer_scheme)],
    responses={401: {"model": ErrorResponse, "description": "Missing or invalid token"}},
)
def me() -> UserOut:
    return UserOut(
        id=1,
        email="stub@example.com",
        full_name="Stub User",
        role=Role.candidate,
        is_active=True,
        created_at=_STUB_TIME,
    )