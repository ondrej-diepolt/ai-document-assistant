from abc import ABC, abstractmethod
from functools import lru_cache

from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"


class EmbeddingClient(ABC):
    """Rozhraní pro embedding poskytovatele (lze vyměnit za OpenAI apod.)."""

    @abstractmethod
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        ...

    def embed_text(self, text: str) -> list[float]:
        return self.embed_texts([text])[0]


class LocalEmbeddingClient(EmbeddingClient):
    def __init__(self, model_name: str = EMBEDDING_MODEL) -> None:
        self._model = SentenceTransformer(model_name)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        vectors = self._model.encode(texts, convert_to_numpy=True)
        return [vector.tolist() for vector in vectors]


@lru_cache
def get_embedding_client() -> EmbeddingClient:
    return LocalEmbeddingClient()