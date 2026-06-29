from app.engine.context import EngineContext
from app.engine.domain_detector import DomainDetector
from app.engine.memory_retriever import MemoryRetriever
from app.engine.prompt_builder import PromptBuilder


class Pipeline:

    def prepare(
        self,
        context: EngineContext,
        user_message: str,
    ) -> EngineContext:

        context.domain = DomainDetector().detect(
            user_message,
        )

        context.memories = MemoryRetriever().retrieve(
            context.user.id,
            context.domain,
        )

        context.system_prompt = PromptBuilder().build(
            context,
        )

        return context