from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.query import QueryRequest, QueryResponse
from app.services import query_service

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
def create_query(payload: QueryRequest, db: Session = Depends(get_db)) -> QueryResponse:
    return query_service.answer_question(db, question=payload.question)