from app.services.user_service import UserService
from app.services.conversation_service import ConversationService
from app.brain.kyroo_brain import kyroo_brain, validate_response


class Orchestrator:

    def __init__(self, db=None):
        self.user_service = UserService(db)
        self.conversation_service = ConversationService(db)

    def process(
        self,
        phone_number: str,
        message: str,
    ) -> str:
        """Process a user message through the full brain pipeline."""

        # 1. Get or create user
        user = self.user_service.get_or_create_user(phone_number)

        # 2. Get recent raw history for the brain
        history = self.conversation_service.get_history_raw(
            user["id"], limit=10
        )

        # 3. Run through THE brain
        result = kyroo_brain(
            user=user,
            message=message,
            history=history,
        )

        # 4. Save user message
        self.conversation_service.add_message(
            user=user,
            role="user",
            content=message,
            module=result.get("module", "general"),
        )

        # 5. Save KIRO response
        self.conversation_service.add_message(
            user=user,
            role="assistant",
            content=result["response"],
            module=result.get("module", "general"),
        )

        return result["response"]