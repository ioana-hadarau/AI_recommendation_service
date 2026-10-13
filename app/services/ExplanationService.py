import json

from app.clients.llm_client import LLMClient
from app.models.JobData import JobData
from app.models.JobPreferences import JobPreferences
from app.models.RecommendationResult import RecommendationResult


class ExplanationService:
    def __init__(self, llm_client: LLMClient) -> None:
        self._llm_client = llm_client

    async def explain(
        self,
        preferences: JobPreferences,
        job: JobData,
        recommendation: RecommendationResult,
    ) -> str:
        payload = {
            "job": job.model_dump(mode="json"),
            "preferences": preferences.model_dump(mode="json"),
            "match": recommendation.model_dump(mode="json"),
        }
        prompt = (
            "Explain this already-calculated job recommendation. "
            "Do not recalculate or change the score, feature values, job ID, "
            "job attributes, or preferences. Do not invent facts. Explain "
            "strengths, weaknesses, and trade-offs in two concise sentences. "
            f"Authoritative data: {json.dumps(payload, sort_keys=True)}"
        )
        return await self._llm_client.explain(prompt)
