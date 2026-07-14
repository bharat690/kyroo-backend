# app/engine/orchestrator.py
import time
from sqlalchemy.orm import Session

from app.brain.conversation_facts import ConversationFacts
from app.brain.conversation_planner import ConversationPlanner, ConversationPlan
from app.brain.bubble_planner import BubblePlanner, BubblePlan
from app.brain.topic_tracker import TopicTracker
from app.brain.relationship_manager import RelationshipManager, RelationshipProfile, RelationshipLevel
from app.brain.detectors.intent import IntentDetector, IntentResult
from app.brain.detectors.emotion import EmotionDetector
from app.brain.style_learner import StyleLearner
from app.brain.response_validator import ResponseValidator
from app.brain.prompt_builder import PromptBuilder

from app.services.memory.service import MemoryService
from app.services.conversation_service import ConversationService
from app.services.user.service import UserService

from app.llm.factory import LLMFactory
from app.models.message import MessageRole


class Orchestrator:

    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)
        self.conversation_service = ConversationService(db)
        self.memory_service = MemoryService(db)
        self.prompt_builder = PromptBuilder()

        self.intent_detector = IntentDetector()
        self.emotion_detector = EmotionDetector()
        self.style_learner = StyleLearner()
        self.conversation_planner = ConversationPlanner()
        self.bubble_planner = BubblePlanner()
        self.response_validator = ResponseValidator()

        self.conversation_facts = {}
        self.topic_trackers = {}
        self.relationship_profiles = {}

    def process(self, phone_number: str, message: str) -> list[str]:
        total_start = time.perf_counter()

        # ── User & Conversation ──
        t = time.perf_counter()
        user = self.user_service.get_or_create_user(phone_number)
        conversation = self.conversation_service.add_message(user, MessageRole.USER, message)
        history = self.conversation_service.history(conversation)
        db_time = time.perf_counter() - t

        # ── State Init ──
        t = time.perf_counter()
        if conversation.id not in self.conversation_facts:
            self.conversation_facts[conversation.id] = ConversationFacts()
        conversation_facts = self.conversation_facts[conversation.id]

        if conversation.id not in self.topic_trackers:
            self.topic_trackers[conversation.id] = TopicTracker()
        topic_tracker = self.topic_trackers[conversation.id]

        if str(user.id) not in self.relationship_profiles:
            self.relationship_profiles[str(user.id)] = RelationshipProfile(
                level=RelationshipLevel.RETURNING
                if self.conversation_service.count_conversations(user) > 1
                else RelationshipLevel.NEW_USER
            )
        relationship_profile = self.relationship_profiles[str(user.id)]
        state_time = time.perf_counter() - t

        # ── Detection ──
        t = time.perf_counter()
        intent_result = self.intent_detector.detect(message, conversation_facts)
        emotion_result = self.emotion_detector.detect_detailed(message)
        style_profile = self.style_learner.learn(history)
        conversation_facts.update_from_message(message, intent_result.intent, intent_result.topic)
        current_topic = topic_tracker.update(message)
        detect_time = time.perf_counter() - t

        # ── Memory ──
        t = time.perf_counter()
        memory_context = self.memory_service.get_context(user.id)
        memory_time = time.perf_counter() - t

        # ── Planning ──
        t = time.perf_counter()
        conversation_plan = self.conversation_planner.plan(
            message=message,
            intent_result=intent_result,
            emotion=emotion_result.emotion,
            style_profile=style_profile,
            conversation_facts=conversation_facts,
        )
        bubble_plan = self.bubble_planner.plan_bubbles(
            behavior=conversation_plan.behavior,
            bubble_count=conversation_plan.bubble_count,
            reply_length=conversation_plan.reply_length,
            ask_question=conversation_plan.ask_question,
            need_tease=conversation_plan.need_tease,
            need_memory=conversation_plan.need_memory,
            need_follow_up=conversation_plan.need_follow_up,
            energy_level=conversation_plan.energy_level,
        )
        plan_time = time.perf_counter() - t

        # ── Prompt Build ──
        t = time.perf_counter()
        prompt = self.prompt_builder.build_with_plans(
            conversation_plan=conversation_plan,
            bubble_plan=bubble_plan,
            intent_result=intent_result,
            emotion_result=emotion_result,
            style_profile=style_profile,
            conversation_facts=conversation_facts,
            topic_tracker=topic_tracker,
            relationship_profile=relationship_profile,
            memory_context=memory_context,
            history=history,
            user_message=message,
        )
        prompt_time = time.perf_counter() - t

        # ── LLM ──
        t = time.perf_counter()
        provider = LLMFactory.create()
        response = provider.generate(prompt)
        reply = response.content
        llm_time = time.perf_counter() - t

        # ── Validation ──
        t = time.perf_counter()
        validated_bubbles = self.response_validator.validate(
            reply,
            plan={
                "emoji_budget": conversation_plan.emoji_budget,
                "reply_length": conversation_plan.reply_length,
            }
        )
        if len(validated_bubbles) > bubble_plan.total_bubbles:
            validated_bubbles = validated_bubbles[:bubble_plan.total_bubbles]
        validate_time = time.perf_counter() - t

        # ── Save ──
        t = time.perf_counter()
        self.conversation_service.add_message(user, MessageRole.ASSISTANT, "\n\n".join(validated_bubbles))
        save_time = time.perf_counter() - t

        # ── Profile ──
        total_time = time.perf_counter() - total_start
        print(
            f"\n⏱ LATENCY: {total_time:.2f}s | "
            f"DB: {db_time:.2f}s | "
            f"State: {state_time:.2f}s | "
            f"Detect: {detect_time:.2f}s | "
            f"Memory: {memory_time:.2f}s | "
            f"Plan: {plan_time:.2f}s | "
            f"Prompt: {prompt_time:.2f}s | "
            f"LLM: {llm_time:.2f}s | "
            f"Validate: {validate_time:.2f}s | "
            f"Save: {save_time:.2f}s"
        )

        return validated_bubbles