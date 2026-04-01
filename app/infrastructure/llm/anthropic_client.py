from typing import Optional

import requests

from app.config import LLM_API_KEY, LLM_BASE_URL, LLM_MAX_TOKENS, LLM_MODEL_NAME, LLM_TEMPERATURE
from app.domain.interfaces import ILLMClient

# JSON schema for a single CV
CV_SCHEMA = {
    "type": "object",
    "properties": {
        "fullname": {"type": "string"},
        "email": {"type": "string"},
        "phone_number": {"type": "string"},
        "dob": {"type": "string"},
        "address": {"type": "string"},
        "gender": {"type": "string"},
        "position": {"type": "string"},
        "note": {"type": "string"},
    },
    "required": ["fullname", "email", "phone_number", "dob", "address", "gender", "position", "note"],
}

# JSON schema for a list of CVs
CV_LIST_SCHEMA = {
    "type": "array",
    "items": CV_SCHEMA,
}


class AnthropicClient(ILLMClient):
    def complete(self, system_prompt: str, user_content: str) -> str:
        if not LLM_API_KEY:
            raise ValueError(
                "LLM_API_KEY is not set. "
                "Set it in .env when using the anthropic provider."
            )
        response = requests.post(
            f"{LLM_BASE_URL}/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": LLM_API_KEY,
                "anthropic-version": "2023-06-01",
            },
            json={
                "model": LLM_MODEL_NAME,
                "max_tokens": LLM_MAX_TOKENS,
                "temperature": LLM_TEMPERATURE,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_content}],
                "output": {"type": "text", "schema": CV_SCHEMA},
            },
        )
        response.raise_for_status()
        result = response.json()
        for block in result.get("content", []):
            if block.get("type") == "text":
                return block["text"]
        raise ValueError("No text block found in Anthropic response")
