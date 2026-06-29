from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class SoftDeleteMixin:

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )