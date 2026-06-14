from abc import ABC, abstractmethod
from functools import lru_cache

from google import genai

from app.core.config import get_settings


class LLMClient(ABC):
    """Rozhraní pro LLM poskytovatele (lze vyměnit za Ollama apod.)."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        ...


class GeminiClient(LLMClient):
    def __init__(self, api_key: str, model: str) -> None:
        self._client = genai.Client(api_key=api_key)
        self._model = model

    def generate(self, prompt: str) -> str:
        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
        )
        return response.text or ""


@lru_cache
def get_llm_client() -> LLMClient:
    settings = get_settings()
    return GeminiClient(api_key=settings.gemini_api_key, model=settings.gemini_model)