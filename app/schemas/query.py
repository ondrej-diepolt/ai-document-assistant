import uuid

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)


class Source(BaseModel):
    document_id: uuid.UUID
    page: int
    text: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]