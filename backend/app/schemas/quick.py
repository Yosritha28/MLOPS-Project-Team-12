from pydantic import BaseModel, Field


class QuickMatchRequest(BaseModel):
    resume_text: str = Field(min_length=20, description="The resume as plain text")
    job_title: str = Field(min_length=1)
    job_text: str = Field(min_length=20, description="The job description as plain text")