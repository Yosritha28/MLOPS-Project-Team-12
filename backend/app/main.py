from fastapi import FastAPI

from app.api import auth

API_PREFIX = "/api/v1"

app = FastAPI(
    title="ResumeIQ API",
    version="1.0.0",
    description=(
        "One REST API for the ResumeIQ web and mobile (PWA) client. "
        "Responses with the header X-Stub: true come from placeholder endpoints "
        "until their real logic is built."
    ),
)


@app.get("/health", tags=["system"], summary="Liveness check")
def health():
    return {"status": "ok", "service": "resumeiq-backend"}


app.include_router(auth.router, prefix=API_PREFIX)