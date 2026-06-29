from sqlalchemy.orm import Session

from app.repositories.memory_repository import MemoryRepository


class MemoryService:

    def __init__(self, db: Session):
        self.repository = MemoryRepository(db)

    def get_context(
        self,
        user_id,
    ) -> str:

        memories = self.repository.get_all(user_id)

        if not memories:
            return "No known memories."

        lines = []

        for memory in memories:
            lines.append(
                f"- {memory.content}"
            )

        return "\n".join(lines)