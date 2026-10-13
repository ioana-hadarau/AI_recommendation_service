from pydantic import BaseModel, Field, model_validator

from app.models.JobData import JobData
from app.models.JobPreferences import JobPreferences


class RecommendationRequest(BaseModel):
    preferences: JobPreferences
    jobs: list[JobData] = Field(min_length=1, max_length=500)
    limit: int = Field(default=10, ge=1, le=100)

    @model_validator(mode="after")
    def validate_unique_jobs(self):
        job_ids = [job.id for job in self.jobs]
        if len(job_ids) != len(set(job_ids)):
            raise ValueError("jobs must not contain duplicate IDs")
        return self
