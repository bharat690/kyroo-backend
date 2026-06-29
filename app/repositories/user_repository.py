from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, phone_number: str) -> User:
        user = User(phone_number=phone_number)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: UUID) -> User | None:
        return self.db.get(User, user_id)

    def get_by_phone(self, phone_number: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.phone_number == phone_number)
            .first()
        )

    def exists(self, phone_number: str) -> bool:
        return (
            self.db.query(User)
            .filter(User.phone_number == phone_number)
            .first()
            is not None
        )

    def update(self, user: User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User):
        self.db.delete(user)
        self.db.commit()