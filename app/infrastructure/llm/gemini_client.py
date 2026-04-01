import requests

from app.config import LLM_API_KEY, LLM_BASE_URL, LLM_MAX_TOKENS, LLM_MODEL_NAME, LLM_TEMPERATURE
from app.domain.interfaces import ILLMClient


class GeminiClient(ILLMClient):
    """Google Gemini via generativelanguage.googleapis.com."""

    def complete(self, system_prompt: str, user_content: str) -> str:
        if not LLM_API_KEY:
            raise ValueError(
                "LLM_API_KEY is not set. "
                "Set it in .env when using the gemini provider."
            )
        response = requests.post(
            (
                f"{LLM_BASE_URL}/v1beta/models/"
                f"{LLM_MODEL_NAME}:generateContent?key={LLM_API_KEY}"
            ),
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": user_content}]}],
                "systemInstruction": {"parts": [{"text": system_prompt}]},
                "generationConfig": {
                    "responseMimeType": "application/json",
                    "maxOutputTokens": LLM_MAX_TOKENS,
                    "temperature": LLM_TEMPERATURE,
                },
            },
        )
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
