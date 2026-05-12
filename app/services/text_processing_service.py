from app.core.logger import get_logger
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = get_logger(__name__)


def split_text_into_chunks(text: str) -> list:
    """
    Splits a long text into smaller overlapping chunks.
    
    chunk_size=300: each chunk is ~300 characters
    chunk_overlap=50: chunks overlap by 50 chars so context isn't lost at boundaries
    """
    logger.info("Splitting text into chunks...")
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=300, chunk_overlap=50)
    
    chunks = splitter.create_documents([text])
    
    logger.info(f"Created {len(chunks)} chunks")
    return chunks