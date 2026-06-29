from dataclasses import dataclass, field

from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message


@dataclass
class EngineContext:

    user: User

    conversation: Conversation

    recent_messages: list[Message] = field(default_factory=list)

    memories: list = field(default_factory=list)

    domain: str = "general"

    system_prompt: str = ""