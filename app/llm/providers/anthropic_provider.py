import anthropic

from app.core.config import settings
from app.llm.base import (
    BaseLLMProvider,
    Prompt,
    LLMResponse,
)


class AnthropicProvider(BaseLLMProvider):

    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=settings.anthropic_api_key,
        )

    def generate(
        self,
        prompt: Prompt,
    ) -> LLMResponse:

        response = self.client.messages.create(
            model=settings.anthropic_model,
            max_tokens=1024,
            system=prompt.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": prompt.user_message,
                }
            ],
        )

        return LLMResponse(
            content=response.content[0].text,
            model=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            finish_reason=response.stop_reason,
        )