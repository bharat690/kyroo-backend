# app/repositories/conversation_repository.py
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.conversation import Conversation


class ConversationRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_id: UUID,
        title: str,
    ) -> Conversation:

        conversation = Conversation(
            user_id=user_id,
            title=title,
        )

        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def get_latest_by_user(
        self,
        user_id: UUID,
    ) -> Conversation | None:

        return (
            self.db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(desc(Conversation.created_at))
            .first()
        )