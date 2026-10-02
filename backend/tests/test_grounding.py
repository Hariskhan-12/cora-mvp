from app.services.grounding import check_grounding


def test_grounded_answer():
    chunks = [
        {"text": "Autonomous vehicles must comply with safety standards for testing on public roads.", "metadata": {}, "relevance": 0.9}
    ]
    answer = "Autonomous vehicles are required to comply with safety standards before they can be tested on public roads."
    assert check_grounding(answer, chunks) is True


def test_refusal_is_not_grounded():
    chunks = [{"text": "some text", "metadata": {}, "relevance": 0.5}]
    answer = "CORA could not find enough supporting information in the available regulatory sources."
    assert check_grounding(answer, chunks) is False


def test_empty_chunks():
    assert check_grounding("some answer", []) is False


def test_ungrounded_answer():
    chunks = [
        {"text": "Regulations about tire pressure monitoring.", "metadata": {}, "relevance": 0.8}
    ]
    answer = "Quantum computing will revolutionize intergalactic spacecraft navigation protocols significantly."
    assert check_grounding(answer, chunks) is False
