from sqlalchemy.orm import Session

from app.db.models import Document


def create_document(
    db: Session, *, filename: str, content_type: str, content: str
) -> Document:
    document = Document(filename=filename, content_type=content_type, content=content)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document