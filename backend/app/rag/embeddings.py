from sentence_transformers import SentenceTransformer
from chromadb import EmbeddingFunction, Documents, Embeddings

from app.core.config import settings


class LocalEmbeddingFunction(EmbeddingFunction):
    """Wraps sentence-transformers so Chroma can call it directly."""

    def __init__(self):
        self._model = SentenceTransformer(settings.embedding_model)

    def __call__(self, input: Documents) -> Embeddings:
        return self._model.encode(input, show_progress_bar=False).tolist()


_instance: LocalEmbeddingFunction | None = None


def get_embedding_function() -> LocalEmbeddingFunction:
    global _instance
    if _instance is None:
        _instance = LocalEmbeddingFunction()
    return _instance
