from app.core.config import settings

from app.llm.providers.anthropic_provider import AnthropicProvider
from app.llm.providers.openai_provider import OpenAIProvider
from app.llm.providers.gemini_provider import GeminiProvider
from app.llm.providers.openrouter_provider import OpenRouterProvider


class LLMFactory:

    @staticmethod
    def create():

        provider = settings.llm_provider.lower()

        providers = {
            "anthropic": AnthropicProvider,
            "openai": OpenAIProvider,
            "gemini": GeminiProvider,
            "openrouter": OpenRouterProvider,
        }

        if provider not in providers:
            raise ValueError(f"Unsupported LLM Provider: {provider}")

        return providers[provider]()