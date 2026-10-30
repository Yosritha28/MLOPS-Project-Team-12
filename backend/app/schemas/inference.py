from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ComponentScores(BaseModel):
    """Used for both component scores and the weights behind them (each 0 to 1)."""

    tfidf: float = Field(ge=0, le=1)
    sbert: float = Field(ge=0, le=1)
    skills: float = Field(ge=0, le=1)


class Explanation(BaseModel):
    summary: str
    strengths: list[str]
    gaps: list[str]


class MatchResult(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    schema_version: str = Field(pattern=r"^[0-9]+\.[0-9]+$", examples=["1.1"])
    overall_score: float = Field(ge=0, le=100)
    component_scores: ComponentScores
    weights: ComponentScores
    matched_skills: list[str]
    missing_skills: list[str]
    explanation: Explanation
    model_version: str = Field(min_length=1)
    latency_ms: float = Field(ge=0)
    warnings: list[str]
    extras: dict[str, Any] | None = None