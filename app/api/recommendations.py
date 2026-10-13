from typing import Annotated

from fastapi import APIRouter, Depends

from app.clients.EmbeddingClient import EmbeddingClient
from app.clients.llm_client import LLMClient
from app.clients.openai_client import OpenAIClient
from app.core.Settings import Settings, get_settings
from app.models.RecommendationResponse import RecommendationResponse
from app.models.recommendationRequest import RecommendationRequest
from app.services.DeterministicMatchingService import DeterministicMatchingService
from app.services.ExplanationService import ExplanationService
from app.services.PreprocessingService import PreprocessingService
from app.services.ScoringService import ScoringService
from app.services.SemanticMatchingService import SemanticMatchingService
from app.services.RecommendationService import RecommendationService


recommendations_router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"],
)


def get_openai_client(
    settings: Annotated[Settings, Depends(get_settings)],
) -> OpenAIClient:
    return OpenAIClient(settings)


def get_recommendation_service(
    openai_client: Annotated[
        OpenAIClient,
        Depends(get_openai_client),
    ],
) -> RecommendationService:
    
    preprocessing_service = PreprocessingService()
    
    embedding_client = EmbeddingClient(
        openai_client.client,
        openai_client.embedding_model,
    )
    
    semantic_service = SemanticMatchingService(
        embedding_client,
        preprocessing_service,
    )
    
    llm_client = LLMClient(
        openai_client.client,
        openai_client.llm_model,
    )
    return RecommendationService(
        semantic_service,
        DeterministicMatchingService(),
        ScoringService(),
        ExplanationService(llm_client),
        preprocessing_service,
    )


@recommendations_router.post(
    "",
    response_model=RecommendationResponse,
    status_code=200,
)
async def generate_recommendations(
    request: RecommendationRequest,
    service: Annotated[
        RecommendationService,
        Depends(get_recommendation_service),
    ],
) -> RecommendationResponse:

    return await service.generate_recommendations(request)