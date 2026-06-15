from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Chunk
from app.services.embedding_client import get_embedding_client


def retrieve_relevant_chunks(
    db: Session, *, question: str, top_k: int = 5
) -> list[Chunk]:
    client = get_embedding_client()
    query_vector = client.embed_text(question)

    distance = Chunk.embedding.cosine_distance(query_vector)
    stmt = select(Chunk).order_by(distance).limit(top_k)

    return list(db.execute(stmt).scalars().all())