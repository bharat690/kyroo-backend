from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.services.user.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/{phone}")
def get_or_create(phone: str, db: Session = Depends(get_db)):
    user = UserService(db).get_or_create_user(phone)

    return {
        "id": str(user.id),
        "phone": user.phone_number,
        "status": user.status.value,
    }