from app.db.models import Chunk
from app.services.prompt_builder import NOT_FOUND_MESSAGE, build_rag_prompt


def _chunk(content: str, page: int) -> Chunk:
    return Chunk(content=content, page_number=page)


def test_prompt_contains_question_and_context():
    chunks = [_chunk("Obsah první pasáže.", 1), _chunk("Obsah druhé pasáže.", 2)]
    prompt = build_rag_prompt("Co to znamená?", chunks)

    assert "Co to znamená?" in prompt
    assert "Obsah první pasáže." in prompt
    assert "(strana 2)" in prompt


def test_prompt_contains_grounding_rules():
    prompt = build_rag_prompt("Otázka?", [_chunk("text", 1)])

    assert NOT_FOUND_MESSAGE in prompt
    assert "POUZE na základě kontextu" in prompt