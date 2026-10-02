import httpx
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


async def chat_completion(system: str, user: str) -> str:
    """Call an OpenAI-compatible chat endpoint."""
    if not settings.llm_api_key:
        raise RuntimeError("LLM_API_KEY is not configured")

    url = f"{settings.llm_base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.llm_model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": settings.llm_temperature,
        "max_tokens": settings.llm_max_tokens,
    }

    async with httpx.AsyncClient(timeout=settings.llm_timeout) as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()

    data = resp.json()
    return data["choices"][0]["message"]["content"]
