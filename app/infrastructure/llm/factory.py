from app.config import LLM_PROVIDER
from app.domain.interfaces import ILLMClient
from app.infrastructure.llm.anthropic_client import AnthropicClient
from app.infrastructure.llm.openai_client import OpenAIClient
from app.infrastructure.llm.gemini_client import GeminiClient


def create_llm_client() -> ILLMClient:
    provider = LLM_PROVIDER.lower()
    if provider == "anthropic":
        return AnthropicClient()
    if provider == "gemini":
        return GeminiClient()
    return OpenAIClient()
