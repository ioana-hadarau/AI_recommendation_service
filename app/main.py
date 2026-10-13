from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from app.api.recommendations import recommendations_router
from app.core.Settings import get_settings
from app.core.exceptions import RecommendationGenerationError


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Internal AI service responsible for generating "
        "job recommendations."
    ),
)


app.include_router(recommendations_router)


@app.get(
    "/health",
    tags=["Health"],
)
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy"
    }
    
@app.exception_handler(RecommendationGenerationError)
async def recommendation_error_handler(
    request: Request,
    exc: RecommendationGenerationError,
) -> JSONResponse:

    return JSONResponse(
        status_code=502,
        content={
            "error": {
                "code": "recommendation_provider_error",
                "message": "Unable to generate recommendations."
            }
        },
    ) 
    
