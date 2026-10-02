"""Tests for retrieval — these require the vector store to be populated."""

import pytest
from app.rag.vectorstore import collection_count


@pytest.fixture
def skip_if_empty():
    if collection_count() == 0:
        pytest.skip("Vector store is empty; run ingestion first.")


def test_collection_accessible():
    count = collection_count()
    assert isinstance(count, int)


def test_retrieval_returns_results(skip_if_empty):
    from app.rag.retriever import retrieve

    chunks, sources = retrieve("autonomous vehicle testing requirements")
    assert len(chunks) > 0
    assert len(sources) > 0
    assert all(s.relevance > 0 for s in sources)


def test_retrieval_irrelevant_query(skip_if_empty):
    from app.rag.retriever import retrieve

    chunks, sources = retrieve("recipe for chocolate cake baking instructions")
    # May still return results but with low relevance; the threshold should filter most
    # We just check the function runs without error
    assert isinstance(chunks, list)


def test_source_metadata(skip_if_empty):
    from app.rag.retriever import retrieve

    chunks, sources = retrieve("California DMV testing permit")
    if sources:
        s = sources[0]
        assert s.title
        assert s.source
