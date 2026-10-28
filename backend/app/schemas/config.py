from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

KEY_PATTERN = r"^[a-z][a-z0-9_]*$"


# ---------- skills ----------
class SkillBase(BaseModel):
    name: str = Field(min_length=1)
    aliases: list[str] = Field(default_factory=list, description="e.g. 'js' for javascript")
    category: str | None = None


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    aliases: list[str] | None = None
    category: str | None = None
    is_active: bool | None = None


class SkillOut(SkillBase):
    id: int
    is_active: bool


# ---------- job fields ----------
class FieldType(str, Enum):
    text = "text"
    number = "number"
    choice = "choice"
    boolean = "boolean"


class JobFieldBase(BaseModel):
    key: str = Field(pattern=KEY_PATTERN, description="Stable machine name, cannot be changed later")
    label: str = Field(min_length=1)
    type: FieldType
    options: list[str] = Field(default_factory=list, description="Allowed values when type is 'choice'")
    required: bool = False
    order: int = 0


class JobFieldCreate(JobFieldBase):
    pass


class JobFieldUpdate(BaseModel):
    """key and type are fixed once created."""

    label: str | None = Field(default=None, min_length=1)
    options: list[str] | None = None
    required: bool | None = None
    order: int | None = None
    is_active: bool | None = None


class JobFieldOut(JobFieldBase):
    id: int
    is_active: bool


# ---------- application statuses ----------
class FeedbackSignal(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"


class StatusBase(BaseModel):
    key: str = Field(pattern=KEY_PATTERN)
    label: str = Field(min_length=1)
    order: int = 0
    feedback: FeedbackSignal = Field(
        default=FeedbackSignal.neutral,
        description="How this status counts as training feedback for retraining",
    )


class StatusCreate(StatusBase):
    pass


class StatusUpdate(BaseModel):
    label: str | None = Field(default=None, min_length=1)
    order: int | None = None
    feedback: FeedbackSignal | None = None
    is_active: bool | None = None


class StatusOut(StatusBase):
    id: int
    is_active: bool


# ---------- scoring ----------
class Weights(BaseModel):
    tfidf: float = Field(ge=0, le=1)
    sbert: float = Field(ge=0, le=1)
    skills: float = Field(ge=0, le=1)

    @model_validator(mode="after")
    def must_sum_to_one(self):
        if abs(self.tfidf + self.sbert + self.skills - 1) > 0.001:
            raise ValueError("weights must sum to 1")
        return self


class ScoringUpdate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    weights: Weights | None = None
    model_version: str | None = Field(default=None, min_length=1)


class ScoringOut(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    weights: Weights
    model_version: str
    updated_at: datetime
    updated_by: int | None = None


class ReloadResponse(BaseModel):
    reloaded: bool
    at: datetime