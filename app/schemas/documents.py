import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentRead(BaseModel):
    id: uuid.UUID
    filename: str
    content_type: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)