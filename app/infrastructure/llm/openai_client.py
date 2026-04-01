import requests

from app.config import LLM_API_KEY, LLM_BASE_URL, LLM_MAX_TOKENS, LLM_MODEL_NAME, LLM_TEMPERATURE
from app.domain.interfaces import ILLMClient


class OpenAIClient(ILLMClient):
    """OpenAI / OpenAI-compatible endpoint (e.g. NCC self-host, vLLM, Azure OpenAI)."""

    def complete(self, system_prompt: str, user_content: str) -> str:
        headers = {"Content-Type": "application/json"}
        if LLM_API_KEY:
            headers["Authorization"] = f"Bearer {LLM_API_KEY}"
        response = requests.post(
            f"{LLM_BASE_URL}/v1/chat/completions",
            headers=headers,
            json={
                "model": LLM_MODEL_NAME,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                'response_format': {
                    'type': 'json_object'
                },
                "max_tokens": LLM_MAX_TOKENS,
                "temperature": LLM_TEMPERATURE,
            },
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
