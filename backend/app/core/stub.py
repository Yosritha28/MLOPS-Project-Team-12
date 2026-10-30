from fastapi import Response


def mark_stub(response: Response) -> None:
    """Temporary scaffolding: placeholder endpoints add the header X-Stub: true."""
    response.headers["X-Stub"] = "true"