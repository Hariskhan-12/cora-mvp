import re


def check_grounding(answer: str, chunks: list[dict]) -> bool:
    """Basic grounding check: does the answer overlap meaningfully with retrieved context?

    This is a simple lexical overlap heuristic for the MVP.
    A production system would use an LLM-as-judge or NLI model.
    """
    if not chunks:
        return False

    refusal_patterns = [
        "not contain enough information",
        "cannot find",
        "no relevant",
        "insufficient",
        "not enough information",
        "do not have enough",
        "unable to find",
    ]
    answer_lower = answer.lower()
    for pattern in refusal_patterns:
        if pattern in answer_lower:
            return False

    context_words = set()
    for chunk in chunks:
        words = set(re.findall(r"\b[a-z]{4,}\b", chunk["text"].lower()))
        context_words.update(words)

    stopwords = {
        "that", "this", "with", "from", "have", "been", "were", "they",
        "their", "which", "would", "could", "should", "about", "into",
        "more", "than", "other", "some", "also", "does", "each", "will",
    }
    context_words -= stopwords

    answer_words = set(re.findall(r"\b[a-z]{4,}\b", answer_lower)) - stopwords
    if not answer_words:
        return False

    overlap = len(answer_words & context_words) / len(answer_words)
    return overlap > 0.25
