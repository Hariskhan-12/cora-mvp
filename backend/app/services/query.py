import logging

from app.models.schemas import QueryResponse
from app.rag.retriever import retrieve
from app.rag.prompts import SYSTEM_PROMPT, USER_TEMPLATE
from app.services.llm import chat_completion
from app.services.grounding import check_grounding

logger = logging.getLogger(__name__)


async def answer_question(question: str) -> QueryResponse:
    chunks, sources = retrieve(question)

    if not chunks:
        return QueryResponse(
            answer=(
                "CORA could not find enough supporting information in the "
                "available regulatory sources to answer this question confidently."
            ),
            sources=[],
            grounded=False,
            chunk_count=0,
        )

    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        meta = chunk["metadata"]
        header = f"[Source {i}: {meta.get('title', 'Unknown')} — {meta.get('section', '')}]"
        context_parts.append(f"{header}\n{chunk['text']}")

    context = "\n\n".join(context_parts)
    user_message = USER_TEMPLATE.format(context=context, question=question)

    answer = await chat_completion(SYSTEM_PROMPT, user_message)
    grounded = check_grounding(answer, chunks)

    return QueryResponse(
        answer=answer,
        sources=sources,
        grounded=grounded,
        chunk_count=len(chunks),
    )
