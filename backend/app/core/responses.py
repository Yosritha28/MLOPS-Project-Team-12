from app.schemas.common import ErrorResponse

UNAUTHORIZED = {401: {"model": ErrorResponse, "description": "Missing or invalid token"}}
FORBIDDEN = {403: {"model": ErrorResponse, "description": "Your role may not do this"}}
NOT_FOUND = {404: {"model": ErrorResponse, "description": "Not found"}}
CONFLICT = {409: {"model": ErrorResponse, "description": "Conflicts with existing data"}}