from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.services.chat_service import (
    save_transcript,
    query_transcripts
)


# -------------------------
# save_transcript
# -------------------------

@patch("app.services.chat_service.split_text_into_chunks")
def test_save_transcript_success(mock_split):

    mock_chunks = ["chunk1", "chunk2"]
    mock_split.return_value = mock_chunks

    mock_vector_store = MagicMock()

    save_transcript(
        transcript="hello world",
        vector_store=mock_vector_store
    )

    mock_split.assert_called_once_with("hello world")

    mock_vector_store.add_documents.assert_called_once_with(
        mock_chunks
    )

@patch("app.services.chat_service.split_text_into_chunks")
def test_save_transcript_failure(mock_split):

    mock_split.return_value = ["chunk1"]

    mock_vector_store = MagicMock()

    mock_vector_store.add_documents.side_effect = Exception(
        "DB failure"
    )

    with pytest.raises(HTTPException) as exc:

        save_transcript(
            transcript="hello",
            vector_store=mock_vector_store
        )

    assert exc.value.status_code == 500
    assert exc.value.detail == "DB failure"


# -------------------------
# query_transcripts
# -------------------------

def test_query_transcripts_empty_collection():

    mock_collection = MagicMock()
    mock_collection.count.return_value = 0

    mock_vector_store = MagicMock()
    mock_vector_store._collection = mock_collection

    with pytest.raises(HTTPException) as exc:

        query_transcripts(
            query="hello",
            prompt="prompt",
            vector_store=mock_vector_store
        )

    assert exc.value.status_code == 400
    assert exc.value.detail == "No transcript loaded."