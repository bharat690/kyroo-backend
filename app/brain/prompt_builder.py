from pathlib import Path

from app.brain.context_builder import ContextBuilder
from app.llm.base import Prompt


class PromptBuilder:

    def __init__(self):

        self.root = (
            Path(__file__).parent / "personality"
        )

        self.context = ContextBuilder()

    def load(self, filename: str) -> str:

        return (
            self.root / filename
        ).read_text(
            encoding="utf-8"
        )

    def build(
        self,
        memory_context: str,
        history,
        user_message: str,
    ) -> Prompt:

        state = self.context.build(user_message)

        GREETINGS = {
            "hi",
            "hii",
            "hiii",
            "hello",
            "heyy",
            "hey",
            "yo",
            "sup",
        }

        is_greeting = (
            user_message.lower().strip() in GREETINGS
        )

        if is_greeting:
            history_text = ""
            memory_context = ""
        else:
            history_text = "\n".join(
                f"{m.role.value}: {m.content}"
                for m in history
            )

        sections = [
            self.load("identity.md"),
            self.load("personality.md"),
            self.load("conversation.md"),
            self.load("relationship.md"),
            self.load("memory.md"),
            self.load("safety.md"),
        ]

        if state.language == "hinglish":
            sections.append(
                self.load("language.md")
            )

        if state.emotion != "neutral":
            sections.append(
                self.load("emotion.md")
            )

        sections.append(
            f"""
        CURRENT STATE

        Language: {state.language}

        Emotion: {state.emotion}

        Topic: {state.topic}

        Relationship: {state.relationship}

        Energy: {state.energy}

        Intent: {state.intent}

        Reply Length: {state.reply_length}

        Ask Question: {state.ask_question}

        Use Memory: {state.use_memory}

        Tease User: {state.tease}

        End Conversation: {state.end_conversation}

        Bubble Count: {state.bubble_count}

        Needs Web Search: {state.needs_web}
        """
        )

        sections.append(
            f"""  
        CURRENT MESSAGE TYPE

        Greeting: {is_greeting}

        If Greeting is True:

        Reply only with a natural greeting.

        Never bring up old conversations.

        Never ask questions.

        Never mention previous topics.



        Priority : Maximum 10 words.

        """
        )

        sections.append(
            f"""
            KNOWN MEMORIES

            {memory_context}
            """
                    )

        sections.append(
                        f"""
            RECENT CHAT

            {history_text}
            """
                    )

        return Prompt(
            system_prompt="\n\n".join(sections),
            user_message=user_message,
        )