from uuid import UUID

from pydantic import BaseModel, Field

from app.models.MatchFeatures import MatchFeatures

class RecommendationResult(BaseModel):
    job_id: UUID
    match_score: float = Field(ge=0.0, le=100.0)
    match_level: str

    features: MatchFeatures

    explanation: str | None = None