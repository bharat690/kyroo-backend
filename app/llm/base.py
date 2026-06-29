from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Prompt:
    system_prompt: str
    user_message: str


@dataclass
class LLMResponse:
    content: str
    model: str
    input_tokens: int
    output_tokens: int
    finish_reason: str | None = None


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate(self, prompt: Prompt) -> LLMResponse:
        pass