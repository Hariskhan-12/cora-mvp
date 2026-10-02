import chromadb
from chromadb.api.models.Collection import Collection

from app.core.config import settings
from app.rag.embeddings import get_embedding_function

_client: chromadb.ClientAPI | None = None
_collection: Collection | None = None


def get_client() -> chromadb.ClientAPI:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
    return _client


def get_collection() -> Collection:
    global _collection
    if _collection is None:
        client = get_client()
        _collection = client.get_or_create_collection(
            name=settings.chroma_collection,
            embedding_function=get_embedding_function(),
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def collection_count() -> int:
    try:
        return get_collection().count()
    except Exception:
        return 0
