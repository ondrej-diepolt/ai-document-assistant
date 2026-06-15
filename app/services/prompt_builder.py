from app.db.models import Chunk

NOT_FOUND_MESSAGE = "Tato informace se v dokumentech nenachází."

SYSTEM_RULES = f"""Jsi asistent, který odpovídá na otázky výhradně na základě poskytnutého kontextu z dokumentů.

Pravidla:
- Odpovídej POUZE na základě kontextu níže. Nepoužívej žádné vlastní ani externí znalosti.
- Pokud odpověď v kontextu není, odpověz přesně: "{NOT_FOUND_MESSAGE}"
- Odpovídej stručně, věcně a česky."""


def build_rag_prompt(question: str, chunks: list[Chunk]) -> str:
    context_blocks = [
        f"[{i}] (strana {chunk.page_number}):\n{chunk.content}"
        for i, chunk in enumerate(chunks, start=1)
    ]
    context = "\n\n".join(context_blocks)

    return (
        f"{SYSTEM_RULES}\n\n"
        f"Kontext:\n{context}\n\n"
        f"Otázka: {question}\n\n"
        f"Odpověď:"
    )