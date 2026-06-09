import logging

from app.api import routes_documents

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.database import get_db

configure_logging()
settings = get_settings()
logger = logging.getLogger(__name__)

logger.info("Starting %s in %s environment", settings.app_name, settings.environment)

app = FastAPI(title=settings.app_name)
app.include_router(routes_documents.router)


@app.get("/health")
def health() -> dict[str, str]:
    logger.debug("Health check requested")
    return {"status": "ok"}


@app.get("/health/db")
def health_db(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}