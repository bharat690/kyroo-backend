# app/brain/detectors/intent.py
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class IntentResult:
    intent: str
    topic: str
    confidence: float
    needs_web: bool
    needs_memory: bool
    needs_tool: bool


class IntentDetector:

    GREETINGS = {
        "hi", "hii", "hiii", "hello", "hey", "heyy", "yo", "sup",
        "good morning", "good evening", "good night", "yooo", "broo",
    }

    GOODBYES = {
        "bye", "goodbye", "see you", "gotta go", "talk later",
        "ttyl", "night", "gn", "bye bye",
    }

    ACKNOWLEDGEMENTS = {
        "fair", "true", "hmm", "hm", "k", "ok", "okay", "nice",
        "cool", "same", "facts", "fr", "for real", "makes sense",
        "right", "yeah", "yea", "yep", "yup", "bet",
    }

    INTENT_PATTERNS: Dict[str, List[str]] = {
        "greeting": ["hi", "hello", "hey", "sup", "yo", "good morning", "good evening", "yooo", "broo", "broski"],
        "goodbye": ["bye", "goodbye", "see you", "gotta go", "talk later", "ttyl", "gn"],
        "acknowledgment": ["fair", "true", "hmm", "ok", "okay", "nice", "cool", "same", "facts", "fr", "bet", "makes sense", "right"],
        "celebration": ["hit ", "achieved", "nailed", "finally ", "passed", "got selected", "got into", "cracked", "cleared", "won", "first time"],
        "recommendation": ["suggest", "recommend", "best", "top", "good", "any good", "what are some", "give me", "list of", "movies to", "shows to", "channels", "headphones", "laptop", "phone", "recipe", "workout routine", "travel", "places to"],
        "information_request": ["what is", "what are", "how does", "how do", "explain", "tell me about", "difference between", "vs", "meaning of", "why does", "how to"],
        "search_request": ["latest", "current", "recent", "news", "today", "who's on", "what happened", "update on"],
        "emotional": ["feel", "feeling", "sad", "happy", "angry", "tired", "exhausted", "stressed", "anxious", "lonely", "depressed", "alone", "overwhelmed", "burnout"],
        "opinion": ["think about", "your opinion", "do you like", "what do you think", "is it worth"],
        "help_request": ["help", "how do i fix", "stuck on", "error", "bug", "not working", "issue with"],
        "memory_query": ["what do you know", "what do you remember", "what's the memory", "do you remember", "you remember"],
        "question": ["?", "how", "what", "why", "when", "where", "who", "can you", "do you"],
    }

    TOPIC_PATTERNS: Dict[str, List[str]] = {
        "general": [],
        "fitness": ["gym", "workout", "exercise", "fitness", "protein", "cardio", "muscle", "weight", "bench", "deadlift", "squat", "chest", "back", "legs"],
        "study": ["study", "learn", "exam", "course", "lecture", "homework", "assignment", "thesis", "research", "gate", "ml", "machine learning", "ai", "deep learning"],
        "coding": ["code", "coding", "programming", "debug", "develop", "software", "app", "website", "api", "python", "javascript", "react", "project"],
        "cooking": ["cook", "recipe", "food", "meal", "kitchen", "ingredient", "bake", "grill", "dish"],
        "entertainment": ["movie", "show", "series", "music", "game", "anime", "netflix", "spotify", "song", "bollywood", "hollywood"],
        "finance": ["money", "expense", "budget", "investment", "salary", "savings", "stock", "crypto"],
        "travel": ["travel", "trip", "vacation", "flight", "hotel", "destination", "visit", "tourist"],
        "health": ["health", "doctor", "medicine", "symptom", "diet", "sleep", "mental health", "wellness"],
        "work": ["work", "office", "meeting", "project", "deadline", "colleague", "boss", "job", "company", "internship"],
        "technology": ["phone", "laptop", "computer", "gadget", "tech", "device", "headphones", "keyboard", "mouse"],
    }

    @classmethod
    def detect(cls, message: str, conversation_facts=None) -> IntentResult:
        lower_msg = message.lower().strip()

        if lower_msg in cls.GREETINGS:
            return IntentResult(
                intent="greeting", topic="general", confidence=0.95,
                needs_web=False, needs_memory=False, needs_tool=False,
            )

        if lower_msg in cls.GOODBYES:
            return IntentResult(
                intent="goodbye", topic="general", confidence=0.95,
                needs_web=False, needs_memory=False, needs_tool=False,
            )

        if lower_msg in cls.ACKNOWLEDGEMENTS:
            return IntentResult(
                intent="acknowledgment", topic="general", confidence=0.9,
                needs_web=False, needs_memory=False, needs_tool=False,
            )

        intent, intent_confidence = cls._detect_intent(lower_msg)
        topic, topic_confidence = cls._detect_topic(lower_msg)
        confidence = (intent_confidence + topic_confidence) / 2
        needs_web = cls._needs_web_search(lower_msg, intent)
        needs_memory = cls._needs_memory(lower_msg, intent, topic, conversation_facts)
        needs_tool = cls._needs_tool(lower_msg, intent, topic)

        return IntentResult(
            intent=intent,
            topic=topic,
            confidence=confidence,
            needs_web=needs_web,
            needs_memory=needs_memory,
            needs_tool=needs_tool,
        )

    @classmethod
    def _detect_intent(cls, message: str) -> Tuple[str, float]:
        # Check high-priority intents first
        priority_intents = ["celebration", "memory_query", "recommendation", "search_request", "information_request"]
        
        for intent in priority_intents:
            patterns = cls.INTENT_PATTERNS[intent]
            score = sum(1 for pattern in patterns if pattern in message)
            if score > 0:
                confidence = min(0.95, 0.7 + score * 0.1)
                return intent, confidence

        intent_scores = {}
        for intent, patterns in cls.INTENT_PATTERNS.items():
            if intent in priority_intents:
                continue
            score = sum(1 for pattern in patterns if pattern in message)
            intent_scores[intent] = score / len(patterns) if patterns else 0

        if not intent_scores or max(intent_scores.values()) == 0:
            return "casual_chat", 0.5

        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        confidence = min(0.9, 0.5 + best_intent[1] * 0.4)
        return best_intent[0], confidence

    @classmethod
    def _detect_topic(cls, message: str) -> Tuple[str, float]:
        topic_scores = {}
        for topic, patterns in cls.TOPIC_PATTERNS.items():
            if topic == "general":
                continue
            score = sum(1 for pattern in patterns if pattern in message)
            if score > 0:
                topic_scores[topic] = score / len(patterns)

        if not topic_scores:
            return "general", 0.7

        best_topic = max(topic_scores.items(), key=lambda x: x[1])
        confidence = min(0.9, 0.6 + best_topic[1] * 0.3)
        return best_topic[0], confidence

    @classmethod
    def _needs_web_search(cls, message: str, intent: str) -> bool:
        if intent in ["search_request", "recommendation"]:
            return True
        web_triggers = ["latest", "current", "recent", "new", "news", "best", "top", "price", "cost"]
        return any(trigger in message for trigger in web_triggers)

    @classmethod
    def _needs_memory(cls, message: str, intent: str, topic: str, conversation_facts) -> bool:
        if intent in ["greeting", "goodbye", "acknowledgment"]:
            return False
        if intent == "memory_query":
            return True
        memory_triggers = ["remember", "last time", "before", "previously", "earlier", "you said", "we talked"]
        return any(trigger in message for trigger in memory_triggers)

    @classmethod
    def _needs_tool(cls, message: str, intent: str, topic: str) -> bool:
        if intent == "recommendation":
            return True
        tool_topics = ["fitness", "cooking", "finance", "travel"]
        if topic in tool_topics and intent in ["help_request", "recommendation"]:
            return True
        return False