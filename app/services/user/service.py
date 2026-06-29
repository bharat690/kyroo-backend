from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def get_or_create_user(self, phone_number: str) -> User:
        user = self.repository.get_by_phone(phone_number)

        if user:
            return user

        return self.repository.create(phone_number)