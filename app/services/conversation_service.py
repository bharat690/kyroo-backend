# app/services/conversation_service.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.models.conversation import Conversation
from app.models.message import Message, MessageRole
from app.models.user import User
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository


class ConversationService:

    def __init__(self, db: Session):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.message_repo = MessageRepository(db)

    def get_or_create_conversation(self, user: User) -> Conversation:
        conversation = (
            self.conversation_repo.get_latest_by_user(user.id)
        )

        if conversation:
            return conversation

        return self.conversation_repo.create(
            user_id=user.id,
            title="New Conversation",
        )

    def add_message(
        self,
        user: User,
        role: MessageRole,
        content: str,
    ) -> Conversation:

        conversation = self.get_or_create_conversation(user)

        self.message_repo.create(
            conversation_id=conversation.id,
            role=role,
            content=content,
        )

        return conversation

    def history(
        self,
        conversation: Conversation,
        limit: int = 20,
    ) -> list[Message]:

        return (
            self.message_repo.get_by_conversation(
                conversation.id,
                limit=limit,
            )
        )

    def count_conversations(self, user: User) -> int:
        return (
            self.db.query(func.count(Conversation.id))
            .filter(Conversation.user_id == user.id)
            .scalar()
            or 0
        )