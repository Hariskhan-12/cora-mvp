from app.core.config import settings
from app.rag.vectorstore import get_collection
from app.models.schemas import Source


def retrieve(query: str) -> tuple[list[dict], list[Source]]:
    """Return (context_chunks, sources) for a query."""
    collection = get_collection()

    results = collection.query(
        query_texts=[query],
        n_results=settings.retrieval_top_k,
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0] if results["documents"] else []
    metadatas = results["metadatas"][0] if results["metadatas"] else []
    distances = results["distances"][0] if results["distances"] else []

    chunks: list[dict] = []
    sources: list[Source] = []
    seen_titles: set[str] = set()

    for doc, meta, dist in zip(documents, metadatas, distances):
        # Chroma cosine distance: 0 = identical, 2 = opposite
        relevance = max(0.0, 1.0 - dist)
        if relevance < settings.relevance_threshold:
            continue

        chunks.append({"text": doc, "metadata": meta, "relevance": relevance})

        title = meta.get("title", "Unknown")
        source_key = f"{title}|{meta.get('section', '')}"
        if source_key not in seen_titles:
            seen_titles.add(source_key)
            sources.append(
                Source(
                    title=title,
                    source=meta.get("source", ""),
                    section=meta.get("section", ""),
                    jurisdiction=meta.get("jurisdiction", ""),
                    relevance=round(relevance, 3),
                )
            )

    sources.sort(key=lambda s: s.relevance, reverse=True)
    return chunks, sources
