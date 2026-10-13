from openai import AsyncOpenAI

from app.core.exceptions import RecommendationGenerationError

# about emebdding servie : https://developers.openai.com/api/reference/ruby/resources/embeddings/methods/create

class EmbeddingClient:

    def __init__(
        self,
        client: AsyncOpenAI,
        model: str,
    ) -> None:
        self._client = client
        self._model = model

    async def create_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        try:
            response = await self._client.embeddings.create(
                model=self._model,
                input=texts,
            )
        except Exception as exc:
            raise RecommendationGenerationError(
                "The embedding provider failed."
            ) from exc

        if len(response.data) != len(texts):
            raise RecommendationGenerationError(
                "The embedding provider returned an invalid response."
            )

        return [
            item.embedding
            for item in response.data
        ]