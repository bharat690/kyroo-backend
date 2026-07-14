# app/brain/conversation_planner.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import random

from app.brain.conversation_facts import ConversationFacts
from app.brain.detectors.intent import IntentResult
from app.brain.style_learner import StyleLearner


SILENT_PRESENCE = [
    "...", "come here 🫂", "i'm here", "those days suck",
    "it's okay to feel that way",
]

GENTLE_FOLLOW_UPS = [
    "was it work ya college?",
    "aaj ka din hi kharab tha kya?",
    "kya hua?",
    "want to talk about it?",
    "long day?",
    "everything okay?",
]


@dataclass
class ConversationPlan:
    reply_length: str
    bubble_count: int
    ask_question: bool
    emoji_budget: int
    need_memory: bool
    need_search: bool
    need_tease: bool
    need_follow_up: bool
    end_conversation: bool
    energy_level: str
    formality: str
    behavior: str
    conversation_goal: str
    keep_alive: bool
    conversation_facts: Optional[ConversationFacts] = None


class ConversationPlanner:

    def plan(
        self,
        message: str,
        intent_result: IntentResult,
        emotion: str,
        style_profile: Dict,
        conversation_facts: Optional[ConversationFacts] = None,
    ) -> ConversationPlan:

        plan = ConversationPlan(
            reply_length="short",
            bubble_count=1,  # DEFAULT 1, not 2
            ask_question=False,
            emoji_budget=1,
            need_memory=intent_result.needs_memory,
            need_search=intent_result.needs_web,
            need_tease=False,
            need_follow_up=False,
            end_conversation=False,
            energy_level="medium",
            formality="casual",
            behavior="react",
            conversation_goal="respond",
            keep_alive=False,
            conversation_facts=conversation_facts,
        )

        handler = getattr(self, f"_handle_{intent_result.intent}", None)
        if handler:
            handler(plan, message, intent_result)
        else:
            self._handle_casual_chat(plan, message, intent_result)

        self._adjust_for_emotion(plan, emotion)
        self._adjust_for_style(plan, style_profile)
        self._decide_keep_alive(plan, message, intent_result, emotion, conversation_facts)

        if conversation_facts:
            self._adjust_for_conversation_facts(plan, conversation_facts)

        return plan

    # ── Intent Handlers ──────────────────────────────

    def _handle_greeting(self, plan, message, intent):
        plan.reply_length = "tiny"
        plan.bubble_count = 1
        plan.ask_question = False
        plan.need_memory = False
        plan.end_conversation = True
        plan.behavior = "acknowledge"
        plan.conversation_goal = "greet"

    def _handle_goodbye(self, plan, message, intent):
        plan.reply_length = "tiny"
        plan.bubble_count = 1
        plan.ask_question = False
        plan.need_memory = False
        plan.end_conversation = True
        plan.behavior = "acknowledge"
        plan.conversation_goal = "end"

    def _handle_acknowledgment(self, plan, message, intent):
        plan.reply_length = "tiny"
        plan.bubble_count = 1
        plan.ask_question = False
        plan.need_memory = False
        plan.behavior = "acknowledge"
        plan.emoji_budget = 0
        if random.random() < 0.4:
            plan.end_conversation = True
        plan.conversation_goal = "acknowledge"

    def _handle_recommendation(self, plan, message, intent):
        plan.conversation_goal = "provide_recommendations"
        plan.reply_length = "medium"
        plan.bubble_count = 1  # single list bubble
        plan.ask_question = False
        plan.need_search = True
        plan.behavior = "provide_info"
        plan.need_follow_up = True

    def _handle_information_request(self, plan, message, intent):
        plan.conversation_goal = "provide_information"
        plan.reply_length = "medium"
        plan.bubble_count = 1
        plan.ask_question = False
        plan.need_search = True
        plan.behavior = "provide_info"

    def _handle_search_request(self, plan, message, intent):
        plan.conversation_goal = "provide_information"
        plan.reply_length = "medium"
        plan.bubble_count = 1
        plan.ask_question = False
        plan.need_search = True
        plan.behavior = "provide_info"

    def _handle_celebration(self, plan, message, intent):
        plan.conversation_goal = "celebrate"
        plan.reply_length = "short"
        plan.bubble_count = 2
        plan.ask_question = False
        plan.energy_level = "high"
        plan.emoji_budget = 2
        plan.behavior = "react_then_observe"

    def _handle_emotional(self, plan, message, intent):
        plan.conversation_goal = "provide_presence"
        plan.reply_length = "short"
        plan.bubble_count = random.choice([1, 2])
        plan.ask_question = False
        plan.energy_level = "low"
        plan.emoji_budget = 1
        plan.behavior = "silent_presence"
        plan.need_tease = False
        plan.need_follow_up = False

    def _handle_memory_query(self, plan, message, intent):
        plan.conversation_goal = "share_memory"
        plan.reply_length = "short"
        plan.bubble_count = 1
        plan.ask_question = False
        plan.need_memory = True
        plan.behavior = "memory_callback"
        plan.need_tease = True

    def _handle_question(self, plan, message, intent):
        plan.conversation_goal = "answer"
        plan.reply_length = "medium"
        plan.bubble_count = 1
        plan.ask_question = False
        plan.need_search = intent.needs_web
        plan.behavior = "provide_info"

    def _handle_opinion(self, plan, message, intent):
        plan.conversation_goal = "share_opinion"
        plan.reply_length = "short"
        plan.bubble_count = 1
        plan.ask_question = False
        plan.behavior = "observation"

    def _handle_help_request(self, plan, message, intent):
        plan.conversation_goal = "provide_help"
        plan.reply_length = "medium"
        plan.bubble_count = 1
        plan.need_search = True
        plan.behavior = "provide_info"

    def _handle_casual_chat(self, plan, message, intent):
        plan.conversation_goal = "respond"
        plan.behavior = random.choice([
            "acknowledge", "react", "observation", "tease",
        ])
        if random.random() < 0.15:
            plan.reply_length = "tiny"
            plan.end_conversation = True

    # ── Keep Alive Logic ─────────────────────────────

    def _decide_keep_alive(self, plan, message, intent, emotion, facts):
        """
        Decide whether to gently continue the conversation
        instead of letting it die.
        """
        # Never keep alive if we're supposed to end
        if plan.end_conversation:
            return

        # Never keep alive for greetings, goodbyes, acknowledgments
        if intent.intent in ["greeting", "goodbye", "acknowledgment"]:
            return

        # Never keep alive for recommendations/info — they have their own follow-up
        if plan.conversation_goal in ["provide_recommendations", "provide_information", "answer"]:
            return

        # If user shares something vulnerable, keep alive with gentle question
        vulnerable_keywords = [
            "exhausting", "tired", "exhausted", "drained", "done with",
            "lonely", "alone", "sad", "depressed", "anxious", "stressed",
            "hate", "sucks", "worst day", "bad day", "rough day",
            "kharab", "thak gaya", "thak gayi", "pareshaan",
        ]

        if any(kw in message.lower() for kw in vulnerable_keywords):
            plan.keep_alive = True
            plan.bubble_count = 2
            plan.ask_question = True
            plan.conversation_goal = "provide_presence_then_ask"
            return

        # If the conversation is very short (first few messages), keep alive
        if facts and facts.message_count <= 4:
            plan.keep_alive = True
            plan.bubble_count = 2
            plan.ask_question = True
            return

        # If user sent something short and open-ended, 30% chance to keep alive
        word_count = len(message.split())
        if word_count <= 5 and random.random() < 0.3:
            plan.keep_alive = True
            plan.bubble_count = 2
            plan.ask_question = True
            return

    # ── Emotion Adjustments ──────────────────────────

    def _adjust_for_emotion(self, plan, emotion):
        if plan.conversation_goal in ["provide_recommendations", "provide_information", "celebrate"]:
            return

        if emotion in ["sad", "angry", "burnout"]:
            plan.energy_level = "low"
            plan.reply_length = "short"
            plan.need_tease = False
            # Don't override keep_alive — it handles the gentle follow-up
            if not plan.keep_alive:
                plan.behavior = "silent_presence"
                plan.conversation_goal = "provide_presence"

        elif emotion == "excited":
            plan.energy_level = "high"
            plan.emoji_budget = max(plan.emoji_budget, 2)

        elif emotion == "anxious":
            plan.energy_level = "low"
            plan.need_tease = False

    # ── Style Adjustments ────────────────────────────

    def _adjust_for_style(self, plan, style_profile):
        if style_profile.get("reply_style") == "tiny":
            plan.reply_length = "tiny"
            plan.bubble_count = 1
        elif style_profile.get("reply_style") == "short":
            if plan.reply_length not in ["tiny"]:
                plan.reply_length = "short"
        elif style_profile.get("reply_style") == "medium":
            if plan.reply_length not in ["tiny", "short"]:
                plan.reply_length = "medium"

        if style_profile.get("emoji_rate") == "low":
            plan.emoji_budget = min(plan.emoji_budget, 1)
        elif style_profile.get("emoji_rate") == "high":
            plan.emoji_budget = min(plan.emoji_budget, 3)

        if style_profile.get("capitalization") == "lower":
            plan.formality = "casual"

    # ── Conversation Facts Adjustments ───────────────

    def _adjust_for_conversation_facts(self, plan, facts):
        if facts.user_question_count > 3:
            plan.ask_question = False
        if facts.message_count > 20:
            if random.random() < 0.3:
                plan.end_conversation = True
        if facts.previous_topic and facts.current_topic != facts.previous_topic:
            plan.need_memory = False