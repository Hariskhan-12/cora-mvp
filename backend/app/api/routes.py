import logging
from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    QueryRequest,
    QueryResponse,
    HealthResponse,
    ErrorResponse,
    Source,
)
from app.services.query import answer_question
from app.rag.vectorstore import collection_count, get_collection
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health():
    count = collection_count()
    return HealthResponse(
        status="ok",
        version=settings.app_version,
        vector_store_ready=count > 0,
        document_count=count,
    )


@router.post(
    "/api/v1/query",
    response_model=QueryResponse,
    responses={400: {"model": ErrorResponse}, 503: {"model": ErrorResponse}},
)
async def query(req: QueryRequest):
    if collection_count() == 0:
        raise HTTPException(503, "Vector store is empty. Run the ingestion script first.")

    if not settings.llm_api_key:
        raise HTTPException(503, "LLM is not configured. Set LLM_API_KEY in .env.")

    try:
        return await answer_question(req.question)
    except RuntimeError as e:
        logger.error("LLM error: %s", e)
        raise HTTPException(503, f"LLM service unavailable: {e}")
    except Exception as e:
        logger.exception("Unexpected error during query")
        raise HTTPException(500, "An internal error occurred. Please try again.")


@router.get("/api/v1/sources", response_model=list[Source])
async def list_sources():
    """Return unique documents in the vector store."""
    collection = get_collection()
    all_meta = collection.get(include=["metadatas"])["metadatas"]

    seen: set[str] = set()
    sources: list[Source] = []
    for meta in all_meta:
        title = meta.get("title", "Unknown")
        if title not in seen:
            seen.add(title)
            sources.append(
                Source(
                    title=title,
                    source=meta.get("source", ""),
                    section=meta.get("document_type", ""),
                    jurisdiction=meta.get("jurisdiction", ""),
                    relevance=1.0,
                )
            )
    return sources
