"""API routes for transcript management and querying."""

from uuid import uuid4

from app.core.logger import get_logger
from app.services.chat_service import query_transcripts, save_transcript
from fastapi import APIRouter, Request

logger = get_logger(__name__)
router = APIRouter()

@router.post('/upload-transcript')
async def upload_transcript(transcript: str, request: Request) -> dict:
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
    
    transcript_id = str(uuid4())
    
    vector_store = request.app.state.vector_store
    save_transcript(transcript, transcript_id, vector_store)

    return {'message': 'Transcript saved successfully!', 
            'transcript_id': transcript_id}

@router.get('/query')
async def query_db(query: str, request: Request, transcript_id: str | None = None) -> str:
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

    response = query_transcripts(query, prompt, vector_store, transcript_id)

    return response

@router.get('/health')
async def health_check():
    logger.info("Health check endpoint called.")
    return {'status': 'ok'}