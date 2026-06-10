from sqlalchemy.orm import Session

from app.db import repositories
from app.db.models import Document
from app.services.pdf_parser import extract_text_from_pdf


def create_document_from_upload(
    db: Session, *, filename: str, content_type: str, data: bytes
) -> Document:
    text = extract_text_from_pdf(data)
    return repositories.create_document(
        db, filename=filename, content_type=content_type, content=text
    )