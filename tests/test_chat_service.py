import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from app.models.transcript_request import TranscriptRequest
from app.services.chat_service import save_transcript, query_transcripts

def test_save_transcript_success():
    mock_vector_store = MagicMock()

    fake_chunks = [MagicMock(), MagicMock()]
    fake_chunks[0].metadata = {}
    fake_chunks[1].metadata = {}

    with patch(
        "app.services.chat_service.split_text_into_chunks",
        return_value=fake_chunks
    ):
        save_transcript(
            transcript=TranscriptRequest(transcript="hello world"),
            transcript_id="abc123",
            vector_store=mock_vector_store
        )

    # ensure metadata was attached
    for chunk in fake_chunks:
        assert chunk.metadata["transcript_id"] == "abc123"

    # ensure DB was called once
    mock_vector_store.add_documents.assert_called_once_with(fake_chunks)

def test_save_transcript_db_failure():
    mock_vector_store = MagicMock()
    mock_vector_store.add_documents.side_effect = Exception("db failure")

    fake_chunks = [MagicMock()]
    fake_chunks[0].metadata = {}

    with patch(
        "app.services.chat_service.split_text_into_chunks",
        return_value=fake_chunks
    ):
        with pytest.raises(HTTPException) as exc:
            save_transcript(
                transcript=TranscriptRequest(transcript="hello"),
                transcript_id="abc",
                vector_store=mock_vector_store
            )

    assert exc.value.status_code == 500
    assert "processing new transcript" in exc.value.detail.lower()

def test_query_transcripts_no_results():
    mock_vector_store = MagicMock()
    mock_vector_store.similarity_search_with_score.return_value = [
        (MagicMock(page_content="irrelevant"), 5.0),
    ]

    with pytest.raises(HTTPException) as exc:
        query_transcripts(
            query="test",
            prompt=MagicMock(),
            vector_store=mock_vector_store
        )

    assert exc.value.status_code == 500