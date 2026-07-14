# app/brain/prompt_builder.py
from pathlib import Path
from typing import Dict, List, Optional

from app.brain.conversation_facts import ConversationFacts
from app.brain.conversation_planner import ConversationPlan
from app.brain.bubble_planner import BubblePlanner, BubblePlan
from app.brain.topic_tracker import TopicTracker
from app.brain.relationship_manager import RelationshipManager, RelationshipProfile
from app.brain.detectors.intent import IntentResult
from app.brain.detectors.emotion import EmotionResult
from app.llm.base import Prompt


GOAL_INSTRUCTIONS = {
    "greet": "Reply with ONLY a natural greeting. No questions. No old topics. Max 10 words.",

    "end": "Reply with a natural goodbye. No questions. Max 8 words.",

    "acknowledge": """Reply with a tiny acknowledgment. Sometimes just an emoji or one word.
Do NOT start a new topic.
40% of the time, just send "..." or "🫂" or nothing extra.""",

    "provide_recommendations": """CRITICAL: Provide the recommendations IMMEDIATELY. Do NOT ask clarifying questions first.
Give 4-6 specific items, one per line, no bullets, no numbers, no markdown.
After listing, you MAY ask a follow-up if keep_alive is true.
NEVER start with "what kind?" or "which type?" — just give options.""",

    "provide_information": """Provide the answer IMMEDIATELY. Do NOT ask clarifying questions first.
Give specific, useful information. No markdown, no bullets, no lists.""",

    "celebrate": """React with high energy first.
Then add value — acknowledge the specific achievement. "that's insane" or "respect".
Do NOT ask "how did you do it?" — just celebrate.""",

    "provide_presence": """Do NOT ask questions. Do NOT give advice.
Be present. Sometimes just "..." or "come here 🫂" or "those days suck".
If you say more, keep it short and warm.
Silence is more human than a paragraph.""",

    "provide_presence_then_ask": """First: acknowledge the feeling. Short, warm. No advice.
Second bubble: ONE gentle, low-pressure question. Examples:
- "was it work ya college?"
- "aaj ka din hi kharab tha kya?"
- "long day?"
Do NOT ask "what happened?" — too broad. Be specific but gentle.
Do NOT give advice. Just show you're here and curious.""",

    "share_memory": """Frame what you know casually, like thinking out loud.
Example: "abhi toh itna hi pata hai... gym jaate ho, coding karte ho. baaki dheere dheere seekh lungi 😭"
NEVER say "kuch nahi hai" or "I don't have any memories."
Even if very little, frame it as "still learning about you" playfully.""",

    "answer": "Answer the question directly. No filler. No 'great question!'. Just the answer.",

    "share_opinion": "Share your opinion directly. Be specific, not generic. No 'I think maybe' — just say it.",

    "provide_help": "Help directly. Don't ask for more context unless absolutely necessary. Give the most likely solution first.",

    "respond": "Respond naturally. Vary between reaction, observation, or tease. Don't always ask questions.",
}


class PromptBuilder:

    def __init__(self):
        self.root = Path(__file__).parent / "personality"
        self.bubble_planner = BubblePlanner()

    def load(self, filename: str) -> str:
        return (self.root / filename).read_text(encoding="utf-8")

    def build_with_plans(
        self,
        conversation_plan: ConversationPlan,
        bubble_plan: BubblePlan,
        intent_result: IntentResult,
        emotion_result: EmotionResult,
        style_profile: Dict,
        conversation_facts: ConversationFacts,
        topic_tracker: TopicTracker,
        relationship_profile: RelationshipProfile,
        memory_context: str,
        history: List,
        user_message: str,
    ) -> Prompt:

        sections = [
            self.load("identity.md"),
            self.load("personality.md"),
            self.load("conversation.md"),
            self.load("relationship.md"),
            self.load("memory.md"),
            self.load("safety.md"),
        ]

        if style_profile.get("hinglish"):
            sections.append(self.load("language.md"))

        if emotion_result.emotion != "neutral":
            sections.append(self.load("emotion.md"))

        # ── Conversation Goal ──
        goal = conversation_plan.conversation_goal
        goal_instruction = GOAL_INSTRUCTIONS.get(goal, GOAL_INSTRUCTIONS["respond"])
        sections.append(f"""
        CONVERSATION GOAL: {goal.upper()}

        {goal_instruction}
        """)

        # ── Relationship ──
        sections.append(f"""
        RELATIONSHIP CONTEXT

        {RelationshipManager.get_relationship_context(relationship_profile)}
        """)

        # ── Plan ──
        sections.append(f"""
        CONVERSATION PLAN

        Reply Length: {conversation_plan.reply_length}
        Energy Level: {conversation_plan.energy_level}
        Behavior: {conversation_plan.behavior}
        Bubble Count: {conversation_plan.bubble_count}
        Emoji Budget: {conversation_plan.emoji_budget}
        Ask Question: {conversation_plan.ask_question}
        Keep Alive: {conversation_plan.keep_alive}
        Use Teasing: {conversation_plan.need_tease}
        Use Memory: {conversation_plan.need_memory}
        End Conversation: {conversation_plan.end_conversation}
        """)

        # ── Bubble Structure ──
        sections.append(f"""
        BUBBLE STRUCTURE

        {self.bubble_planner.get_bubble_context(bubble_plan)}

        Separate bubbles with double newlines.
        """)

        # ── Intent & Topic ──
        sections.append(f"""
        INTENT: {intent_result.intent}
        TOPIC: {intent_result.topic}
        """)

        # ── Style ──
        sections.append(f"""
        USER STYLE

        Emoji: {style_profile.get('emoji_rate', 'low')}
        Length: {style_profile.get('reply_style', 'short')}
        Caps: {style_profile.get('capitalization', 'lower')}
        Hinglish: {style_profile.get('hinglish', False)}
        Gen Z: {style_profile.get('genz', False)}
        Mirror naturally. Never more expressive than the user.
        """)

        # ── Facts ──
        sections.append(f"""
        CONVERSATION FACTS

        {conversation_facts.get_context_string()}
        """)

        # ── Topic ──
        sections.append(f"""
        TOPIC CONTEXT

        {topic_tracker.get_topic_context()}
        """)

        # ── Memories ──
        sections.append(f"""
        KNOWN MEMORIES

        {memory_context}
        """)

        # ── History ──
        history_text = "\n".join(
            f"{m.role.value}: {m.content}"
            for m in history[-10:]
        )
        sections.append(f"""
        RECENT CHAT

        {history_text}
        """)

        return Prompt(
            system_prompt="\n\n".join(sections),
            user_message=user_message,
        )