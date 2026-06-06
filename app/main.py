import logging

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()
settings = get_settings()
logger = logging.getLogger(__name__)

logger.info("Starting %s in %s environment", settings.app_name, settings.environment)

app = FastAPI(title=settings.app_name)


@app.get("/health")
def health() -> dict[str, str]:
    logger.debug("Health check requested")
    return {"status": "ok"}