from uuid import UUID

from sqlalchemy.orm import Session

from app.models.conversation import Conversation


class ConversationRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: UUID) -> Conversation:
        conversation = Conversation(user_id=user_id)

        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def latest(self, user_id: UUID) -> Conversation | None:
        return (
            self.db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
            .first()
        )