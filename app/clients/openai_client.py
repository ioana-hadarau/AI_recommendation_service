from openai import AsyncOpenAI

from app.core.Settings import Settings


class OpenAIClient:
    def __init__(self, settings: Settings) -> None:
        self._client = AsyncOpenAI(
            api_key=settings.openai_api_key,
        )

        self._embedding_model = settings.openai_embedding_model
        self._llm_model = settings.openai_model

    @property
    def client(self) -> AsyncOpenAI:
        return self._client

    @property
    def embedding_model(self) -> str:
        return self._embedding_model

    @property
    def llm_model(self) -> str:
        return self._llm_model