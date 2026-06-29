from app.llm.base import BaseLLMProvider, LLMResponse


class OpenAIProvider(BaseLLMProvider):

    def generate(
        self,
        system_prompt: str,
        messages: list[dict],
    ) -> LLMResponse:

        raise NotImplementedError