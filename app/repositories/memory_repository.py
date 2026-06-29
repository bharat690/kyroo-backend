from uuid import UUID

from sqlalchemy.orm import Session

from app.models.memory import Memory


class MemoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(
        self,
        user_id: UUID,
        category: str,
        content: str,
        importance: int = 5,
    ) -> Memory:

        memory = Memory(
            user_id=user_id,
            category=category,
            content=content,
            importance=importance,
        )

        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)

        return memory

    def get_all(
        self,
        user_id: UUID,
    ) -> list[Memory]:

        return (
            self.db.query(Memory)
            .filter(Memory.user_id == user_id)
            .order_by(Memory.importance.desc())
            .all()
        )