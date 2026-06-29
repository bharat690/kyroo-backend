from uuid import UUID

from sqlalchemy.orm import Session

from app.models.message import Message, MessageRole


class MessageRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(
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

    def history(
        self,
        conversation_id: UUID,
        limit: int = 20,
    ):

        return (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
            .all()
        )