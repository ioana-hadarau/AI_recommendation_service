from uuid import UUID

from app.clients.EmbeddingClient import EmbeddingClient
from app.models.JobData import JobData
from app.models.JobPreferences import JobPreferences
from app.core.exceptions import RecommendationGenerationError
from app.services.PreprocessingService import PreprocessingService
from app.services.SimilarityMethods import cosine_similarity


class SemanticMatchingService:
    def __init__(
        self,
        embedding_client: EmbeddingClient,
        preprocessing_service: PreprocessingService,
    ) -> None:
        
        self._preprocessing = preprocessing_service

        self._embedding_client = embedding_client

    async def calculate_title_matches(
        self,
        preferences: JobPreferences,
        jobs: list[JobData],
    ) -> dict[UUID, float | None]:
        
        preferred_title = self._preprocessing.normalize_text(
            preferences.preferred_title
        )
        if preferred_title is None:
            return {job.id: None for job in jobs}

        job_titles = [
            self._preprocessing.normalize_text(job.title) or ""
            for job in jobs
        ]
        embeddings = await self._embedding_client.create_embeddings(
            [preferred_title, *job_titles]
        )
        preference_embedding = embeddings[0]
        try:
            return {
                job.id: cosine_similarity(preference_embedding, embeddings[index])
                for index, job in enumerate(jobs, start=1)
            }
        except ValueError as exc:
            raise RecommendationGenerationError(
                "The embedding provider returned incompatible vectors."
            ) from exc
