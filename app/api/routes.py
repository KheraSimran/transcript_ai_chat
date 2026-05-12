"""API routes for transcript management and querying."""

from app.core.logger import get_logger
from app.services.chat_service import query_transcripts, save_transcript
from fastapi import APIRouter, Request

logger = get_logger(__name__)
router = APIRouter()

@router.post('/upload-transcript')
async def upload_transcript(transcript: str, request: Request) -> str:
    """Upload and index transcript content for querying.

    Args:
        transcript: The raw transcript text to be saved.
        request: The FastAPI request object containing app state.

    Returns:
        A success message indicating the transcript was saved.

    Raises:
        HTTPException: If transcript ingestion fails.
    """
    logger.info("Upload transcript endpoint called.")

    vector_store = request.app.state.vector_store
    save_transcript(transcript, vector_store)

    return 'Transcript saved successfully!'

@router.get('/query')
async def query_db(query: str, request: Request) -> str:
    """Query the transcript database and generate a response.

    Args:
        query: The user-provided query string.
        request: The FastAPI request object containing app state.

    Returns:
        The generated response string based on the query.

    Raises:
        HTTPException: If the query processing fails.
    """
    logger.info("Query database endpoint called.")

    vector_store = request.app.state.vector_store
    prompt = request.app.state.rag_prompt

    response = query_transcripts(query, prompt, vector_store)

    return response

@router.get('/health')
async def health_check():
    logger.info("Health check endpoint called.")
    return {'status': 'ok'}