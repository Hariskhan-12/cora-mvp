# CORA — Autonomous Vehicle Regulatory Intelligence

CORA is an AI-powered research tool that helps users understand autonomous vehicle regulations. Ask a question about AV regulations, and CORA retrieves relevant information from a curated set of regulatory documents and generates a grounded answer with source citations.

## What this MVP demonstrates

- RAG (Retrieval-Augmented Generation) pipeline over regulatory documents
- Vector search with Chroma and sentence-transformers embeddings
- LLM-generated answers constrained to retrieved context
- Source attribution and basic grounding validation
- Clean, responsive UI for the query/answer workflow

This is a demonstration MVP — not a production regulatory tool. The dataset is a small, summarized collection based on publicly available regulatory information.

## Architecture

```
User → React UI → FastAPI → Query Embedding → Chroma Vector Search
                                                     ↓
                                              Retrieved Context
                                                     ↓
                                           Groq LLM (Llama 3.3)
                                                     ↓
                                         Grounding Check → Answer + Sources
```

**Backend:** Python, FastAPI, Chroma, sentence-transformers, httpx  
**Frontend:** React, TypeScript, Vite  
**LLM:** Groq API (GPT OSS 120B) — any OpenAI-compatible endpoint works  
**Embeddings:** all-MiniLM-L6-v2 (local, open-source)

## Running locally

### Prerequisites

- Python 3.11+
- Node.js 18+
- A Groq API key (free at https://console.groq.com)

### Backend

```bash
cd cora-mvp/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env       # Windows
# cp .env.example .env       # macOS/Linux

# Edit .env and add your Groq API key:
#   LLM_API_KEY=gsk_your_key_here

# Ingest regulatory documents into vector store
python -m scripts.ingest

# Start the API server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd cora-mvp/frontend

npm install
npm run dev
```

Open http://localhost:5173 in your browser.

### Environment variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LLM_API_KEY` | Yes | — | Groq API key |
| `LLM_BASE_URL` | No | `https://api.groq.com/openai/v1` | OpenAI-compatible endpoint |
| `LLM_MODEL` | No | `openai/gpt-oss-120b` | Model identifier |
| `LLM_TEMPERATURE` | No | `0.1` | Generation temperature |
| `LLM_MAX_TOKENS` | No | `1024` | Max response tokens |
| `DEBUG` | No | `false` | Enable debug logging |

## Ingesting documents

The demo dataset is in `backend/data/documents/`. To ingest:

```bash
cd cora-mvp/backend
python -m scripts.ingest
```

The script loads JSON documents, chunks the text, generates embeddings, and stores everything in a local Chroma database. The vector store persists in `backend/data/chroma_db/`.

To add new documents, create a JSON file in the same format as the existing ones and re-run ingestion.

## Running tests

```bash
cd cora-mvp/backend
pip install pytest
pytest tests/ -v
```

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check, vector store status |
| `POST` | `/api/v1/query` | Submit a regulatory question |
| `GET` | `/api/v1/sources` | List available documents |

## Known limitations

- The regulatory dataset is a small summarized demo — not comprehensive or authoritative.
- Grounding validation is a simple lexical overlap heuristic; a production system would use NLI or an LLM judge.
- No conversation history or follow-up questions.
- No authentication or rate limiting.
- Chunking is word-based, not token-based.
- The embedding model (all-MiniLM-L6-v2) is lightweight and good for the MVP but not the highest-quality option for production use.
