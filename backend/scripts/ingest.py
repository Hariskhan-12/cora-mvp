"""Ingest regulatory documents into the Chroma vector store.

Run from the backend directory:
    python -m scripts.ingest
"""

import json
import hashlib
import sys
from pathlib import Path

# Ensure the backend root is on the path so `app.*` imports resolve.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
from app.rag.vectorstore import get_collection
from app.rag.embeddings import get_embedding_function


DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "documents"


def chunk_text(text: str, max_tokens: int, overlap: int) -> list[str]:
    """Split text into overlapping chunks by approximate word count."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + max_tokens
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap
    return chunks


def build_chunk_id(title: str, section: str, index: int) -> str:
    raw = f"{title}|{section}|{index}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def ingest():
    collection = get_collection()
    json_files = list(DATA_DIR.glob("*.json"))

    if not json_files:
        print(f"No JSON files found in {DATA_DIR}")
        return

    total_chunks = 0

    for fpath in json_files:
        print(f"Processing {fpath.name}...")
        documents: list[dict] = json.loads(fpath.read_text(encoding="utf-8"))

        for doc in documents:
            title = doc["title"]
            source = doc["source"]
            jurisdiction = doc.get("jurisdiction", "")
            document_type = doc.get("document_type", "")
            demo_note = doc.get("demo_note", "")

            for section_obj in doc["sections"]:
                section = section_obj["section"]
                text = section_obj["text"]

                chunks = chunk_text(text, settings.chunk_size, settings.chunk_overlap)

                for i, chunk in enumerate(chunks):
                    chunk_id = build_chunk_id(title, section, i)
                    metadata = {
                        "title": title,
                        "source": source,
                        "jurisdiction": jurisdiction,
                        "document_type": document_type,
                        "section": section,
                        "chunk_index": i,
                        "demo_note": demo_note,
                    }

                    collection.upsert(
                        ids=[chunk_id],
                        documents=[chunk],
                        metadatas=[metadata],
                    )
                    total_chunks += 1

    print(f"Ingested {total_chunks} chunks into collection '{settings.chroma_collection}'.")
    print(f"Collection now has {collection.count()} total chunks.")


if __name__ == "__main__":
    ingest()
