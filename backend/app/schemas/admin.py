from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.auth import Role


class UserUpdate(BaseModel):
    is_active: bool | None = None
    role: Role | None = None


class ModelStage(str, Enum):
    production = "production"
    staging = "staging"
    archived = "archived"


class ModelVersionOut(BaseModel):
    version: str
    stage: ModelStage
    metrics: dict[str, float] = Field(
        default_factory=dict, description="Evaluation metrics logged in MLflow"
    )
    created_at: datetime


class ModelReloadResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    reloaded: bool
    model_version: str
    at: datetime


class DriftStatus(str, Enum):
    ok = "ok"
    warning = "warning"
    alert = "alert"


class SystemStats(BaseModel):
    requests_last_24h: int
    error_rate: float = Field(ge=0, le=1)
    p50_latency_ms: float
    p95_latency_ms: float


class DriftOut(BaseModel):
    status: DriftStatus
    drifted_features: list[str]
    last_checked_at: datetime | None = None


class MonitoringOut(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model_version: str
    system: SystemStats
    drift: DriftOut
    last_retrained_at: datetime | None = None


class FairnessCheck(BaseModel):
    name: str
    description: str
    value: float
    threshold: float
    passed: bool


class FairnessOut(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model_version: str
    evaluated_at: datetime | None = None
    checks: list[FairnessCheck]