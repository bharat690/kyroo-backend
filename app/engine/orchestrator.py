from sqlalchemy.orm import Session
from context import EngineContext
from pipeline import Pipeline
from message_formatter import MessageFormatter
from app.models.message import MessageRole
from app.services.user.service import UserService
from app.services.conversation_service import ConversationService
from app.llm.factory import LLMFactory




class Orchestrator:

    def __init__(self, db: Session):

        self.user_service = UserService(db)
        self.conversation_service = ConversationService(db)

    def process(
        self,
        phone_number: str,
        message: str,
    ) -> str:

        user = self.user_service.get_or_create_user(phone_number)

        conversation = self.conversation_service.add_message(
            user,
            MessageRole.USER,
            message,
        )

        history = self.conversation_service.history(conversation)

        memory_context = self.memory_service.get_context(
            user.id
        )

        prompt = self.prompt_builder.build(
            memory_context=memory_context,
            history=history,
            user_message=message,
        )

        provider = LLMFactory.create()

        response = provider.generate(prompt)

        reply = response.content

        self.conversation_service.add_message(
            user,
            MessageRole.ASSISTANT,
            reply,
        )

        return reply