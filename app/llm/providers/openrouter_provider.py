from app.llm.base import BaseLLMProvider, LLMResponse


class OpenRouterProvider(BaseLLMProvider):

    def generate(
        self,
        system_prompt: str,
        messages: list[dict],
    ) -> LLMResponse:

        raise NotImplementedError