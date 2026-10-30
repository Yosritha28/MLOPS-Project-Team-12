# # from fastapi import FastAPI
# #
# # from app.api import admin_config, auth, config, jobs, resumes
# #
# # API_PREFIX = "/api/v1"
# #
# # app = FastAPI(
# #     title="ResumeIQ API",
# #     version="1.0.0",
# #     description=(
# #         "One REST API for the ResumeIQ web and mobile (PWA) client. "
# #         "Responses with the header X-Stub: true come from placeholder endpoints "
# #         "until their real logic is built."
# #     ),
# # )
# #
# #
# # @app.get("/health", tags=["system"], summary="Liveness check")
# # def health():
# #     return {"status": "ok", "service": "resumeiq-backend"}
# #
# #
# # app.include_router(auth.router, prefix=API_PREFIX)
# # app.include_router(config.router, prefix=API_PREFIX)
# # app.include_router(admin_config.router, prefix=API_PREFIX)
# # app.include_router(resumes.router, prefix=API_PREFIX)
# # app.include_router(jobs.router, prefix=API_PREFIX)
#
#
#
# from fastapi import FastAPI
# from fastapi.responses import PlainTextResponse
#
# from app.api import admin, admin_config, analysis, applications, auth, config, jobs, resumes
#
# API_PREFIX = "/api/v1"
#
# app = FastAPI(
#     title="ResumeIQ API",
#     version="1.0.0",
#     description=(
#         "One REST API for the ResumeIQ web and mobile (PWA) client. "
#         "Responses with the header X-Stub: true come from placeholder endpoints "
#         "until their real logic is built."
#     ),
# )
#
#
# @app.get("/health", tags=["system"], summary="Liveness check")
# def health():
#     return {"status": "ok", "service": "resumeiq-backend"}
#
#
# @app.get(
#     "/metrics",
#     tags=["system"],
#     summary="Prometheus metrics (placeholder until the real exporter is added)",
#     response_class=PlainTextResponse,
# )
# def metrics() -> PlainTextResponse:
#     body = (
#         "# HELP resumeiq_up 1 if the API is running\n"
#         "# TYPE resumeiq_up gauge\n"
#         "resumeiq_up 1\n"
#     )
#     return PlainTextResponse(body)
#
#
# app.include_router(auth.router, prefix=API_PREFIX)
# app.include_router(config.router, prefix=API_PREFIX)
# app.include_router(admin_config.router, prefix=API_PREFIX)
# app.include_router(admin.router, prefix=API_PREFIX)
# app.include_router(resumes.router, prefix=API_PREFIX)
# app.include_router(jobs.router, prefix=API_PREFIX)
# app.include_router(applications.router, prefix=API_PREFIX)
# app.include_router(analysis.router, prefix=API_PREFIX)

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, PlainTextResponse, RedirectResponse

from app.api import admin, admin_config, analysis, applications, auth, config, jobs, quick, resumes

API_PREFIX = "/api/v1"
STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(
    title="ResumeIQ API",
    version="1.0.0",
    description=(
        "One REST API for the ResumeIQ web and mobile (PWA) client. "
        "Responses with the header X-Stub: true come from placeholder endpoints "
        "until their real logic is built."
    ),
)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/demo")


@app.get("/demo", include_in_schema=False)
def demo():
    return FileResponse(STATIC_DIR / "demo.html")


@app.get("/health", tags=["system"], summary="Liveness check")
def health():
    return {"status": "ok", "service": "resumeiq-backend"}


@app.get(
    "/metrics",
    tags=["system"],
    summary="Prometheus metrics (placeholder until the real exporter is added)",
    response_class=PlainTextResponse,
)
def metrics() -> PlainTextResponse:
    body = (
        "# HELP resumeiq_up 1 if the API is running\n"
        "# TYPE resumeiq_up gauge\n"
        "resumeiq_up 1\n"
    )
    return PlainTextResponse(body)


app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(config.router, prefix=API_PREFIX)
app.include_router(admin_config.router, prefix=API_PREFIX)
app.include_router(admin.router, prefix=API_PREFIX)
app.include_router(resumes.router, prefix=API_PREFIX)
app.include_router(jobs.router, prefix=API_PREFIX)
app.include_router(applications.router, prefix=API_PREFIX)
app.include_router(analysis.router, prefix=API_PREFIX)
app.include_router(quick.router, prefix=API_PREFIX)