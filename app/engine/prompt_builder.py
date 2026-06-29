from app.llm.base import Prompt
from app.models.message import Message


class PromptBuilder:

    def build(
        self,
        memory_context: str,
        history: list[Message],
        user_message: str,
    ) -> Prompt:

        conversation = []

        for msg in history:
            role = "User" if msg.role.value == "user" else "Kyroo"
            conversation.append(f"{role}: {msg.content}")

        history_text = "\n".join(conversation)

        system_prompt = f"""
You are Kyroo.

You are a WhatsApp-native AI life companion.

Never mention you are ChatGPT, Claude or an AI assistant.

Speak naturally.

Use the memories when relevant.

=====================
KNOWN MEMORIES
=====================

{memory_context}

=====================
RECENT CONVERSATION
=====================

{history_text}
"""

        return Prompt(
            system_prompt=system_prompt,
            user_message=user_message,
        )