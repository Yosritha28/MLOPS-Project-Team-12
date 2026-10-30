# from datetime import datetime, timezone
#
# from app.schemas.inference import ComponentScores, Explanation, MatchResult
# from app.schemas.jobs import JobOut
# from app.schemas.resumes import ResumeOut, ResumeStatus
#
# STUB_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)
#
#
# def sample_match() -> MatchResult:
#     return MatchResult(
#         schema_version="1.1",
#         overall_score=78.4,
#         component_scores=ComponentScores(tfidf=0.61, sbert=0.83, skills=0.75),
#         weights=ComponentScores(tfidf=0.3, sbert=0.5, skills=0.2),
#         matched_skills=["python", "sql", "docker"],
#         missing_skills=["kubernetes"],
#         explanation=Explanation(
#             summary="Strong match on core Python and data skills; missing container orchestration.",
#             strengths=["3 years of relevant experience"],
#             gaps=["No Kubernetes experience listed"],
#         ),
#         model_version="hybrid-v1",
#         latency_ms=142,
#         warnings=[],
#     )
#
#
# def sample_job(job_id: int = 1) -> JobOut:
#     return JobOut(
#         id=job_id,
#         recruiter_id=1,
#         title="Data Engineer",
#         description="Build and maintain data pipelines.",
#         required_skills=["python", "sql", "docker", "kubernetes"],
#         preferred_skills=["airflow"],
#         min_experience_years=2,
#         education_level="Bachelor",
#         custom_fields={"salary": 1200000, "location": "Hyderabad", "remote": True},
#         is_open=True,
#         created_at=STUB_TIME,
#         updated_at=STUB_TIME,
#     )
#
#
# def sample_resume(resume_id: int = 1) -> ResumeOut:
#     return ResumeOut(
#         id=resume_id,
#         candidate_id=1,
#         filename="resume.pdf",
#         content_type="application/pdf",
#         size_bytes=120000,
#         status=ResumeStatus.parsed,
#         skills=["python", "sql", "docker"],
#         total_experience_years=3,
#         warnings=[],
#         uploaded_at=STUB_TIME,
#     )


from datetime import datetime, timezone

from app.schemas.applications import ApplicationDetail, ApplicationOut, MyApplicationOut
from app.schemas.auth import Role, UserOut
from app.schemas.inference import ComponentScores, Explanation, MatchResult
from app.schemas.jobs import JobOut
from app.schemas.resumes import ResumeOut, ResumeStatus

STUB_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def sample_match() -> MatchResult:
    return MatchResult(
        schema_version="1.1",
        overall_score=78.4,
        component_scores=ComponentScores(tfidf=0.61, sbert=0.83, skills=0.75),
        weights=ComponentScores(tfidf=0.3, sbert=0.5, skills=0.2),
        matched_skills=["python", "sql", "docker"],
        missing_skills=["kubernetes"],
        explanation=Explanation(
            summary="Strong match on core Python and data skills; missing container orchestration.",
            strengths=["3 years of relevant experience"],
            gaps=["No Kubernetes experience listed"],
        ),
        model_version="hybrid-v1",
        latency_ms=142,
        warnings=[],
    )


def sample_job(job_id: int = 1) -> JobOut:
    return JobOut(
        id=job_id,
        recruiter_id=1,
        title="Data Engineer",
        description="Build and maintain data pipelines.",
        required_skills=["python", "sql", "docker", "kubernetes"],
        preferred_skills=["airflow"],
        min_experience_years=2,
        education_level="Bachelor",
        custom_fields={"salary": 1200000, "location": "Hyderabad", "remote": True},
        is_open=True,
        created_at=STUB_TIME,
        updated_at=STUB_TIME,
    )


def sample_resume(resume_id: int = 1) -> ResumeOut:
    return ResumeOut(
        id=resume_id,
        candidate_id=1,
        filename="resume.pdf",
        content_type="application/pdf",
        size_bytes=120000,
        status=ResumeStatus.parsed,
        skills=["python", "sql", "docker"],
        total_experience_years=3,
        warnings=[],
        uploaded_at=STUB_TIME,
    )


def sample_user(user_id: int = 1, role: Role = Role.candidate) -> UserOut:
    return UserOut(
        id=user_id,
        email=f"user{user_id}@example.com",
        full_name=f"User {user_id}",
        role=role,
        is_active=True,
        created_at=STUB_TIME,
    )


def sample_application(application_id: int = 1, job_id: int = 1, resume_id: int = 1) -> ApplicationOut:
    return ApplicationOut(
        id=application_id,
        job_id=job_id,
        candidate_id=1,
        resume_id=resume_id,
        status_key="applied",
        status_reason=None,
        match_score=78.4,
        applied_at=STUB_TIME,
        updated_at=STUB_TIME,
    )


def sample_my_application(application_id: int = 1) -> MyApplicationOut:
    base = sample_application(application_id)
    return MyApplicationOut(**base.model_dump(), job_title="Data Engineer", match=sample_match())


def sample_detail(application_id: int = 1, rank: int = 1) -> ApplicationDetail:
    base = sample_application(application_id)
    return ApplicationDetail(
        **base.model_dump(),
        rank=rank,
        candidate_name=f"Candidate {application_id}",
        resume_skills=["python", "sql", "docker"],
        total_experience_years=3,
        match=sample_match(),
    )