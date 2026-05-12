# Python Documentation Standards (Production Grade)

Use these rules when generating documentation for Python backend services.

The goal:

- Short
- Clear
- Maintainable
- Useful for other developers
- Production-grade
- No unnecessary explanations

---

# General Rules

## Write documentation for:

- Public functions
- Service methods
- API routes
- Complex logic
- Non-obvious business decisions
- Classes
- Important configuration

Do NOT document:

- Obvious code
- Simple getters/setters
- Every single variable
- Trivial one-line functions
- Comments that repeat the code

Bad:

```python
# Increment counter
counter += 1
```

---

# Preferred Docstring Style

Use Google-style docstrings.

Example:

```python
def save_transcript(transcript: str, vector_store: Chroma) -> None:
    """Split and store a transcript in the vector database.

    Args:
        transcript: Raw transcript text.
        vector_store: Initialized Chroma vector store.

    Raises:
        HTTPException: If document ingestion fails.
    """
```

---

# Function Documentation Rules

## Keep first line short

The first sentence should explain:

- what the function does
- not how it works internally

Good:

```python
"""Query transcript chunks using a RAG pipeline."""
```

Bad:

```python
"""This function takes the query, initializes the retriever,
creates a language model, formats the documents, and returns
an answer from the chain."""
```

---

# Route Documentation

Document:

- endpoint purpose
- important request data
- possible errors

Example:

```python
@router.post('/upload-transcript')
async def upload_transcript(...):
    """Upload and index transcript content for querying.

    Raises:
        HTTPException: If transcript ingestion fails.
    """
```

---

# Service Layer Documentation

Focus on:

- business responsibility
- side effects
- external dependencies

Example:

```python
def query_transcripts(...) -> str:
    """Generate an answer using transcript context from ChromaDB.

    The function retrieves relevant transcript chunks and sends
    them through a LangChain RAG pipeline.

    Raises:
        HTTPException: If the transcript database is empty or
            the query pipeline fails.
    """
```

---

# Inline Comments

Use inline comments sparingly.

Only comment:

- Why something exists
- Architectural decisions
- Performance tradeoffs
- Workarounds
- Non-obvious logic

---

# Module-Level Documentation

Every important module should have a short top-level description.

Example:

```python
"""Service layer for transcript ingestion and RAG querying."""
```

---

# Exception Documentation

Document meaningful exceptions only.

Good:

```python
Raises:
    HTTPException: If no transcript exists in the collection.
```

Avoid documenting generic exceptions unless important.

---

# Production Documentation Principles

Documentation should answer:

1. What does this component do?
2. Why does it exist?
3. What are the important inputs/outputs?
4. What failures matter?

It should NOT:

- narrate every line
- explain basic Python
- duplicate type hints
- become longer than the code itself

---

# Preferred Documentation Structure

For production backend projects:

1. Module docstring
2. Imports
3. Constants
4. Classes/functions with docstrings
5. Minimal inline comments

---

# Example Production-Grade Function

```python
"""Transcript query service using LangChain and ChromaDB."""

from fastapi import HTTPException


def query_transcripts(
    query: str,
    prompt: str,
    vector_store: Chroma
) -> str:
    """Generate an answer using transcript context.

    Retrieves relevant transcript chunks from ChromaDB and
    executes a LangChain RAG pipeline.

    Args:
        query: User question.
        prompt: LangChain prompt template.
        vector_store: Configured Chroma vector store.

    Returns:
        Generated response string.

    Raises:
        HTTPException: If the database is empty or the
            RAG pipeline fails.
    """

    collection = vector_store._collection

    if collection.count() == 0:
        raise HTTPException(
            status_code=400,
            detail="No transcript loaded."
        )
```

---

# Copilot Instruction Rules

When generating documentation:

- Prefer concise wording
- Use Google-style docstrings
- Avoid redundant comments
- Explain intent, not syntax
- Keep comments production-grade
- Avoid tutorial-style explanations
- Keep line lengths readable
- Assume experienced backend developers will read the code
- Prioritize maintainability over verbosity
