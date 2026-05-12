"""Main application entry point for Transcript AI Chat.

This module initializes the FastAPI application, sets up the application
lifespan, and includes API routes for transcript management and querying.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from langchain_classic import hub
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from app.core.config import settings
from app.api.routes import router

COLLECTION_NAME = 'transcript_db'

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes the vector store and RAG prompt during the application lifespan.

    Args:
        app: The FastAPI application instance.

    Yields:
        None: Allows the application to run within the context.
    """
    embedding = OpenAIEmbeddings()
    app.state.vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embedding,
            host=settings.chroma_host,
            port=settings.chroma_port
    )
    app.state.rag_prompt = hub.pull('rlm/rag-prompt')

    yield

app = FastAPI(title='Transcript AI Chat', 
              description='Chat with your transcripts', 
              version='1.0.0',
              lifespan=lifespan)
app.include_router(router, prefix='/api')

@app.get('/')
async def root():
    return {
        'message': 'Transcript AI Chat is running',
        'docs': '/docs'
    }
