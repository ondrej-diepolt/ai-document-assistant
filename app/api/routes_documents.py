from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db import repositories
from app.db.database import get_db
from app.schemas.documents import DocumentRead

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
def upload_document(
    file: UploadFile,
    db: Session = Depends(get_db),
) -> DocumentRead:
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported.",
        )

    document = repositories.create_document(
        db,
        filename=file.filename or "unknown.pdf",
        content_type=file.content_type,
    )
    return document