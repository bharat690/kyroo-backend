from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.enums import UserStatus
from app.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    phone_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    status: Mapped[UserStatus] = mapped_column(
    Enum(
        UserStatus,
        name="user_status",
        values_callable=lambda enum: [e.value for e in enum],
    ),
    default=UserStatus.ACTIVE,
    nullable=False,
    )

    conversations = relationship(
    "Conversation",
    back_populates="user",
    cascade="all, delete-orphan",
    )
    memories = relationship(
        "Memory",
        cascade="all, delete-orphan",
    )