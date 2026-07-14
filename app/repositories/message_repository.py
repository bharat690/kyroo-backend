# app/repositories/message_repository.py
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.message import Message, MessageRole


class MessageRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        conversation_id: UUID,
        role: MessageRole,
        content: str,
    ) -> Message:

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def get_by_conversation(
        self,
        conversation_id: UUID,
        limit: int = 20,
    ) -> list[Message]:

        return (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(desc(Message.created_at))
            .limit(limit)
            .all()[::-1]
        )