from fastapi import APIRouter, Depends, Query

from app.core.responses import FORBIDDEN, NOT_FOUND, UNAUTHORIZED
from app.core.samples import STUB_TIME, sample_user
from app.core.security import bearer_scheme
from app.core.stub import mark_stub
from app.schemas.admin import (
    DriftOut,
    DriftStatus,
    FairnessCheck,
    FairnessOut,
    ModelReloadResponse,
    ModelStage,
    ModelVersionOut,
    MonitoringOut,
    SystemStats,
    UserUpdate,
)
from app.schemas.auth import Role, UserOut
from app.schemas.common import Page

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(mark_stub), Depends(bearer_scheme)],
    responses={**UNAUTHORIZED, **FORBIDDEN},
)


@router.get("/users", response_model=Page[UserOut], summary="All users")
def list_users(
    role: Role | None = None,
    is_active: bool | None = None,
    q: str | None = Query(None, description="Search in name and email"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> Page[UserOut]:
    return Page[UserOut](items=[sample_user()], total=1, page=page, page_size=page_size)


@router.patch(
    "/users/{user_id}",
    response_model=UserOut,
    summary="Activate, deactivate or change the role of a user",
    responses=NOT_FOUND,
)
def update_user(user_id: int, body: UserUpdate) -> UserOut:
    return sample_user(user_id).model_copy(update=body.model_dump(exclude_unset=True))


@router.get("/models", response_model=list[ModelVersionOut], summary="Model versions from the registry")
def list_models() -> list[ModelVersionOut]:
    return [
        ModelVersionOut(
            version="hybrid-v1",
            stage=ModelStage.production,
            metrics={"ndcg_at_10": 0.82, "p95_latency_ms": 180.0},
            created_at=STUB_TIME,
        )
    ]


@router.post(
    "/models/reload",
    response_model=ModelReloadResponse,
    summary="Reload the production model from the registry without a redeploy",
)
def reload_model() -> ModelReloadResponse:
    return ModelReloadResponse(reloaded=True, model_version="hybrid-v1", at=STUB_TIME)


@router.get("/monitoring", response_model=MonitoringOut, summary="System health and data drift")
def monitoring() -> MonitoringOut:
    return MonitoringOut(
        model_version="hybrid-v1",
        system=SystemStats(requests_last_24h=1200, error_rate=0.004, p50_latency_ms=95.0, p95_latency_ms=210.0),
        drift=DriftOut(status=DriftStatus.ok, drifted_features=[], last_checked_at=STUB_TIME),
        last_retrained_at=STUB_TIME,
    )


@router.get("/fairness", response_model=FairnessOut, summary="Latest fairness evaluation")
def fairness() -> FairnessOut:
    return FairnessOut(
        model_version="hybrid-v1",
        evaluated_at=STUB_TIME,
        checks=[
            FairnessCheck(
                name="name_swap",
                description="Largest score change when only the candidate name is swapped",
                value=0.4,
                threshold=2.0,
                passed=True,
            )
        ],
    )