from sqlalchemy.orm import Session

from app.schemas.query import QueryResponse, Source
from app.services.llm_client import get_llm_client
from app.services.prompt_builder import NOT_FOUND_MESSAGE, build_rag_prompt
from app.services.retrieval_service import retrieve_relevant_chunks


def answer_question(db: Session, *, question: str, top_k: int = 5) -> QueryResponse:
    chunks = retrieve_relevant_chunks(db, question=question, top_k=top_k)

    if not chunks:
        return QueryResponse(answer=NOT_FOUND_MESSAGE, sources=[])

    prompt = build_rag_prompt(question, chunks)
    answer = get_llm_client().generate(prompt)

    if answer.strip() == NOT_FOUND_MESSAGE:
        return QueryResponse(answer=NOT_FOUND_MESSAGE, sources=[])

    sources = [
        Source(document_id=c.document_id, page=c.page_number, text=c.content)
        for c in chunks
    ]
    return QueryResponse(answer=answer, sources=sources)