import os
from typing import Set

from dotenv import load_dotenv

load_dotenv()

LLM_API_URL: str = os.getenv("LLM_API_URL", "https://api-llm.nccsoft.vn/v1/chat/completions")
LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "Qwen3.5-35B-A3B")
LLM_MAX_TOKENS: int = 8192
LLM_TEMPERATURE: float = 0.2

ALLOWED_EXTENSIONS: Set[str] = {"doc", "docx", "pdf"}
