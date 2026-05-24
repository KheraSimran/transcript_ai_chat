"""Service layer for transcript ingestion and RAG querying."""

from fastapi import HTTPException
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from app.core.logger import get_logger
from langchain_core.output_parsers import StrOutputParser
from app.services.text_processing_service import split_text_into_chunks

logger = get_logger(__name__)

def save_transcript(transcript: str, transcript_id: str, vector_store: Chroma):
    """Split and store a transcript with id in the vector database.

    Args:
        transcript: Raw transcript text.
        transcript_id: uuid string id.
        vector_store: Initialized Chroma vector store.

    Raises:
        HTTPException: If document ingestion fails.
    """
    logger.info("Process new transcript...")
    chunks = split_text_into_chunks(transcript)

    for chunk in chunks:
        chunk.metadata = {
            "transcript_id": transcript_id
        }
    try:
        logger.info("Saving new transcript chunks into vector store.")
        vector_store.add_documents(chunks)
        logger.info("Transcript successfully saved to vector store.")
    except Exception as e:
        logger.exception("Error saving new transcript.")
        raise HTTPException(status_code=500, detail="Error while processing new transcript.")

def query_transcripts(query: str, prompt: str, vector_store: Chroma, transcript_id: str | None = None) -> str:
    """Generate an answer using transcript context from ChromaDB.

    The function retrieves relevant transcript chunks and sends
    them through a LangChain RAG pipeline.

    Args:
        query: User question.
        prompt: LangChain prompt template.
        vector_store: Configured Chroma vector store.
        transcript_id: optional transcript uuid for filtering.

    Returns:
        Generated response string.

    Raises:
        HTTPException: If the transcript database is empty or
            the query pipeline fails.
    """
    logger.info("Querying transcripts...")
    
    try:
        transcript_filter = {}
        if transcript_id:
            transcript_filter["transcript_id"] = transcript_id

        docs_and_scores = vector_store.similarity_search_with_score(query, k=3, filter=transcript_filter if transcript_filter else None)

        logger.info("Context documents retrieved successfully.")

        seen = set()
        unique_docs = []
        for doc, score in docs_and_scores:
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                unique_docs.append((doc, score))

        SCORE_TRESHOLD = 1.1

        score_filtered_docs = [doc for doc, score in unique_docs
                         if score <= SCORE_TRESHOLD]
        
        logger.info("Documents cleaned and filtered successfully.")

        if not score_filtered_docs:
            logger.warning(
                "No relevant transcript chunks found. Scores: %s",
                [score for _, score in unique_docs]
            )
            raise HTTPException(status_code=400, detail="No relevant transcript content found.")
        
        context = "\n\n".join(doc.page_content for doc in score_filtered_docs)

        logger.info("Retrieved %d relevant chunks.", len(score_filtered_docs))

        # The lower the temperature, the more strict the model is to the context
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        rag_chain = (
            prompt
            | llm
            | StrOutputParser()
        )

        response = rag_chain.invoke({
            "context": context,
            "question": query
        })
        logger.info("Query successfully processed.")
        return response
    except Exception as e:
            logger.exception("Error during query processing")
            raise HTTPException(status_code=500, detail="Error processing query")
