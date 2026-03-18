import requests

from app.config import LLM_API_URL, LLM_MAX_TOKENS, LLM_MODEL_NAME, LLM_TEMPERATURE
from app.domain.interfaces import ILLMClient


class LLMClient(ILLMClient):
    def __init__(self) -> None:
        self._url = LLM_API_URL
        self._model = LLM_MODEL_NAME
        self._headers = {"Content-Type": "application/json"}

    def complete(self, system_prompt: str, user_content: str) -> str:
        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            "max_tokens": LLM_MAX_TOKENS,
            "temperature": LLM_TEMPERATURE,
        }
        response = requests.post(self._url, headers=self._headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
