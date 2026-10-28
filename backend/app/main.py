from fastapi import FastAPI

from app.api import admin_config, auth, config, jobs, resumes

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
app.include_router(config.router, prefix=API_PREFIX)
app.include_router(admin_config.router, prefix=API_PREFIX)
app.include_router(resumes.router, prefix=API_PREFIX)
app.include_router(jobs.router, prefix=API_PREFIX)