from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.message import MessageRole
from app.models.user import User

from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository


class ConversationService:

    def __init__(self, db: Session):
        self.conversations = ConversationRepository(db)
        self.messages = MessageRepository(db)

    def get_or_create_conversation(
        self,
        user: User,
    ) -> Conversation:

        conversation = self.conversations.latest(user.id)

        if conversation is None:
            conversation = self.conversations.create(user.id)

        return conversation

    def add_message(
        self,
        user: User,
        role: MessageRole,
        content: str,
    ) -> Conversation:

        conversation = self.get_or_create_conversation(user)

        self.messages.save(
            conversation.id,
            role,
            content,
        )

        return conversation

    def history(
        self,
        conversation: Conversation,
    ):
        return self.messages.history(conversation.id)