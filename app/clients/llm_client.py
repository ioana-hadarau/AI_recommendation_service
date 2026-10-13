from openai import AsyncOpenAI

from app.core.exceptions import RecommendationGenerationError


class LLMClient:
    def __init__(self, client: AsyncOpenAI, model: str) -> None:
        self._client = client
        self._model = model

    async def explain(self, prompt: str) -> str:
        try:
            response = await self._client.responses.create(
                model=self._model,
                input=prompt,
            )
            return response.output_text
        except Exception as exc:
            raise RecommendationGenerationError(
                "The explanation provider failed."
            ) from exc
