import uuid
from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    __tablename__ = "messages"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role: Mapped[MessageRole] = mapped_column(
        SqlEnum(
            MessageRole,
            values_callable=lambda x: [e.value for e in x],
            name="message_role",
        ),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )