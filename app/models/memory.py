import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Memory(BaseModel):
    __tablename__ = "memories"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    importance: Mapped[int] = mapped_column(
        Integer,
        default=5,
        nullable=False,
    )