from sqlalchemy.orm import Session

from app.models.message import MessageRole
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository


class ConversationService:

    def __init__(self, db: Session):

        self.conversations = ConversationRepository(db)
        self.messages = MessageRepository(db)

    def history(self, conversation):
        return self.messages.history(conversation.id)

    def add_message(
        self,
        user,
        role: MessageRole,
        content: str,
    ):

        conversation = self.conversations.latest(user.id)

        if conversation is None:
            conversation = self.conversations.create(user.id)

        self.messages.save(
            conversation.id,
            role,
            content,
        )

        return conversation