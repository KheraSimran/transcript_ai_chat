# Transcript RAG AI App

## Overview

This project is a full-stack Retrieval-Augmented Generation (RAG) application that allows users to query across transcript data using natural language. It combines a FastAPI backend with a JavaScript frontend, and uses vector search (ChromaDB) + LLMs (OpenAI) to answer questions grounded in stored transcript content.

The system is designed to support searching across large transcript datasets and answering questions with context-aware responses.

## Tech Stack

**Backend**

- Python
- LangChain
- RAG
- ChromaDB (vector database)
- FastAPI
- OpenAI API
- Pydantic Settings
- Uvicorn

**Frontend**

- JavaScript
- Fetch API for backend communication

**Infrastructure**

- Docker
- GitHub Actions (CI/CD)
- Render (deployment)

## Features

- Natural language question answering over transcripts
- Semantic search using embeddings
- Context-aware LLM responses
- Multi-transcript support
- REST API backend
- Simple frontend chat/query interface
- CI pipeline for backend tests + frontend build validation
- Deployment via Render

## Running Locally

### Backend

````bash
cd transcript_ai_chat
pip install -r requirements.txt
uvicorn app.main:app --reload
# or if using docker
docker compose up --build

### Frontend

```bash
cd frontend
npm install
npm run dev
````

## CI/CD Pipeline

GitHub Actions pipeline:

- Runs backend tests using pytest
- Validates Python dependencies
- Builds frontend using `npm ci` + `npm run build`
- Deploys backend to Render via deploy hook (on main branch only)

## Testing

Backend tests are executed with:

```bash
pytest tests/ -v
```

Note: Frontend currently has no automated tests. Build step is used as validation.

## Deployment

### Backend (Render)

- Deployed via Render service
- Triggered through GitHub Actions deploy hook
- Environment variables configured in Render dashboard

### Frontend

- Built using Vite
- Static build deployed separately (Render or static hosting)
- Requires correct `VITE_API_BASE` for API routing

## Known Limitations

- No frontend test suite yet
- No reranking layer in retrieval pipeline
- Chunk-level embedding may cause topic dominance issues
- No authentication layer currently implemented

## Future Improvements

- Query decomposition for multi-intent questions
- Hybrid retrieval (BM25 + embeddings)
- Reranking layer for better context selection
- Frontend testing (Vitest / Playwright)
- Authentication and user-level transcript isolation

## Notes

This system relies heavily on embedding similarity for retrieval. Query structure and chunking strategy significantly affect output quality, especially when multiple unrelated questions are asked in a single prompt.
