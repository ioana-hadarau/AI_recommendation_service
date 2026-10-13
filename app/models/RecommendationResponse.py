from pydantic import BaseModel

from app.models.RecommendationResult import RecommendationResult


class RecommendationResponse(BaseModel):
    recommendations: list[RecommendationResult]
