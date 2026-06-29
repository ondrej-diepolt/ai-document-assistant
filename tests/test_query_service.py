import uuid

from app.db.models import Chunk
from app.services import query_service
from app.services.prompt_builder import NOT_FOUND_MESSAGE


class FakeLLM:
    """Falešný LLM klient — vrátí předem danou odpověď, nevolá API."""

    def __init__(self, answer: str) -> None:
        self._answer = answer

    def generate(self, prompt: str) -> str:
        return self._answer


def _chunk(content: str, page: int) -> Chunk:
    return Chunk(document_id=uuid.uuid4(), content=content, page_number=page)


def test_relevant_answer_returns_sources(monkeypatch):
    chunks = [_chunk("Relevantní pasáž.", 3)]
    monkeypatch.setattr(
        query_service, "retrieve_relevant_chunks",
        lambda db, *, question, top_k: chunks,
    )
    monkeypatch.setattr(
        query_service, "get_llm_client", lambda: FakeLLM("Toto je odpověď."),
    )

    result = query_service.answer_question(db=None, question="Otázka?")

    assert result.answer == "Toto je odpověď."
    assert len(result.sources) == 1
    assert result.sources[0].page == 3


def test_not_found_answer_returns_no_sources(monkeypatch):
    chunks = [_chunk("Nesouvisející pasáž.", 1)]
    monkeypatch.setattr(
        query_service, "retrieve_relevant_chunks",
        lambda db, *, question, top_k: chunks,
    )
    monkeypatch.setattr(
        query_service, "get_llm_client", lambda: FakeLLM(NOT_FOUND_MESSAGE),
    )

    result = query_service.answer_question(db=None, question="Něco mimo?")

    assert result.answer == NOT_FOUND_MESSAGE
    assert result.sources == []


def test_no_chunks_skips_llm(monkeypatch):
    monkeypatch.setattr(
        query_service, "retrieve_relevant_chunks",
        lambda db, *, question, top_k: [],
    )

    def fail() -> None:
        raise AssertionError("LLM se nemá volat, když nejsou chunky")

    monkeypatch.setattr(query_service, "get_llm_client", fail)

    result = query_service.answer_question(db=None, question="Cokoli?")

    assert result.answer == NOT_FOUND_MESSAGE
    assert result.sources == []