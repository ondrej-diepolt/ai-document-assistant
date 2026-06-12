import uuid

from sqlalchemy.orm import Session

from app.db import repositories
from app.db.models import Chunk, Document
from app.services.chunking import chunk_text
from app.services.pdf_parser import extract_pages
from app.services.embedding_client import get_embedding_client


def create_document_from_upload(
    db: Session, *, filename: str, content_type: str, data: bytes
) -> Document:
    pages = extract_pages(data)
    full_text = "\n".join(pages)

    document = repositories.create_document(
        db, filename=filename, content_type=content_type, content=full_text
    )

    chunks = _build_chunks(document.id, pages)
    if chunks:
        _attach_embeddings(chunks)
        repositories.create_chunks(db, chunks)

    return document


def _build_chunks(document_id: uuid.UUID, pages: list[str]) -> list[Chunk]:
    chunks: list[Chunk] = []
    index = 0
    for page_number, page_text in enumerate(pages, start=1):
        for piece in chunk_text(page_text):
            chunks.append(
                Chunk(
                    document_id=document_id,
                    chunk_index=index,
                    page_number=page_number,
                    content=piece,
                )
            )
            index += 1
    return chunks

def _attach_embeddings(chunks: list[Chunk]) -> None:
    client = get_embedding_client()
    vectors = client.embed_texts([chunk.content for chunk in chunks])
    for chunk, vector in zip(chunks, vectors, strict=True):
        chunk.embedding = vector