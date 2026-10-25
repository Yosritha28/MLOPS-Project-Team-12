from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorResponse(BaseModel):
    """Every error from the API has this shape."""

    detail: str
    code: str


class Page(BaseModel, Generic[T]):
    """Every list endpoint returns this shape."""

    items: list[T]
    total: int
    page: int
    page_size: int