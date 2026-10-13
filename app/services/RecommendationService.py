
from app.models.MatchFeatures import MatchFeatures
from app.models.RecommendationResult import RecommendationResult
from app.models.recommendationRequest import RecommendationRequest
from app.models.RecommendationResponse import RecommendationResponse
from app.services.DeterministicMatchingService import DeterministicMatchingService
from app.services.ExplanationService import ExplanationService
from app.services.PreprocessingService import PreprocessingService
from app.services.ScoringService import ScoringService, get_match_level
from app.services.SemanticMatchingService import SemanticMatchingService


class RecommendationService:

    def __init__(
        self,
        semantic_matching_service: SemanticMatchingService,
        deterministic_matching_service: DeterministicMatchingService,
        scoring_service: ScoringService,
        explanation_service: ExplanationService,
        preprocessing_service: PreprocessingService,
    ) -> None:
        self._semantic = semantic_matching_service
        self._deterministic = deterministic_matching_service
        self._scoring = scoring_service
        self._explanation = explanation_service
        self._preprocessing = preprocessing_service
 
    def _normalize_preferences(self, request: RecommendationRequest):
        
        preferences = request.preferences.model_copy(deep=True)
       
        for field_name in (
            "preferred_title",
            "preferred_company_name",
            "location",
            "country",
        ):
            setattr(
                preferences,
                field_name,
                self._preprocessing.normalize_text(
                    getattr(preferences, field_name)
                ),
            )
        return preferences

    def _normalize_job(self, job):
        
        normalized_job = job.model_copy(deep=True)
        
        for field_name in ("title", "company_name", "location", "country"):
            setattr(
                normalized_job,
                field_name,
                self._preprocessing.normalize_text(
                    getattr(normalized_job, field_name)
                ),
            )
        return normalized_job

    @staticmethod
    def _company_similarity(preference: str | None, company: str) -> float | None:
        
        if preference is None:
            return None
        return 1.0 if preference == company else 0.0   
    
    
    
    
    
    async def generate_recommendations(
    self,
        request: RecommendationRequest,
    ) -> RecommendationResponse:
        
        preferences = self._normalize_preferences(request)
        
        jobs = [self._normalize_job(job) for job in request.jobs]
        
        semantic_results = await self._semantic.calculate_title_matches(
            preferences,
            jobs,
        )
        results: list[RecommendationResult] = []

        for job in jobs:
            features = MatchFeatures(
                title_similarity=semantic_results[job.id],
                company_similarity=self._company_similarity(
                    preferences.preferred_company_name,
                    job.company_name,
                ),
                **self._deterministic.calculate_features(preferences, job),
            )
            score = self._scoring.calculate(features)
            results.append(
                RecommendationResult(
                    job_id=job.id,
                    match_score=score,
                    match_level=get_match_level(score),
                    features=features,
                )
            )

        results.sort(key=lambda item: (-item.match_score, str(item.job_id)))
        selected = results[: request.limit]
        jobs_by_id = {job.id: job for job in jobs}
        for result in selected:
            result.explanation = await self._explanation.explain(
                preferences,
                jobs_by_id[result.job_id],
                result,
            )

        return RecommendationResponse(recommendations=selected)
