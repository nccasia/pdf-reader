import os
from typing import Set

from dotenv import load_dotenv

load_dotenv()

LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "https://api-llm.nccsoft.vn")
LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "Qwen3.5-35B-A3B")
LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "8192"))
LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.2"))
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")

ALLOWED_EXTENSIONS: Set[str] = {"doc", "docx", "pdf"}
