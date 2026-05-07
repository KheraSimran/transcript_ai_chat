from fastapi import APIRouter
from app.core.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.get('/health')
async def health_check():
    logger.info("Health check endpoint called.")
    return {'status': 'ok'}