"""Service layer for transcript ingestion and RAG querying."""

from fastapi import HTTPException
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from app.core.logger import get_logger
from langchain_core.output_parsers import StrOutputParser
from app.services.text_processing_service import split_text_into_chunks

logger = get_logger(__name__)

def save_transcript(transcript: str, vector_store: Chroma):
    """Split and store a transcript in the vector database.

    Args:
        transcript: Raw transcript text.
        vector_store: Initialized Chroma vector store.

    Raises:
        HTTPException: If document ingestion fails.
    """
    logger.info("Saving transcript to vector store.")
    chunks = split_text_into_chunks(transcript)

    try:
        vector_store.add_documents(chunks)
        logger.info("Transcript successfully saved to vector store.")
    except Exception as e:
        logger.error(f"Error saving transcript: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def query_transcripts(query: str, prompt: str, vector_store: Chroma) -> str:
    """Generate an answer using transcript context from ChromaDB.

    The function retrieves relevant transcript chunks and sends
    them through a LangChain RAG pipeline.

    Args:
        query: User question.
        prompt: LangChain prompt template.
        vector_store: Configured Chroma vector store.

    Returns:
        Generated response string.

    Raises:
        HTTPException: If the transcript database is empty or
            the query pipeline fails.
    """
    logger.info("Querying transcripts.")
    
    # Check for empty database
    collection = vector_store._collection
    if collection.count() == 0:
        logger.warning("No transcripts found in vector store.")
        raise HTTPException(status_code=400, detail="No transcript loaded.")

    retriever = vector_store.as_retriever(search_kwargs={'k': 3})

    # The lower the temperature, the more strict the model is to the context
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    
    # Post-processing
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    rag_chain = ({
        'context': retriever | format_docs,
        'question':  RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    try:
        response = rag_chain.invoke(query)
        logger.info("Query successfully processed.")
        return response
    except Exception as e:
        logger.error(f"Error during query processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))
