from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import re

@dataclass
class ConversationFacts:
    """
    Maintains temporary conversation state that lives only for the current conversation.
    This helps avoid using outdated assumptions in responses.
    """
    # User activities
    coded_today: Optional[bool] = None
    went_gym: Optional[bool] = None
    studied_today: Optional[bool] = None
    cooked_today: Optional[bool] = None
    
    # Current state
    current_activity: Optional[str] = None
    current_emotion: Optional[str] = None
    current_topic: Optional[str] = None
    previous_topic: Optional[str] = None
    
    # Conversation flow
    message_count: int = 0
    questions_asked: int = 0
    user_question_count: int = 0
    
    # Facts mentioned
    mentioned_facts: Dict[str, Any] = field(default_factory=dict)
    invalidated_facts: set = field(default_factory=set)
    
    def update_from_message(self, message: str, intent: str, topic: str):
        """Update facts based on the current message."""
        self.message_count += 1
        lower_msg = message.lower()
        
        # Track topic changes
        if self.current_topic and self.current_topic != topic:
            self.previous_topic = self.current_topic
        self.current_topic = topic
        
        # Check for negations
        has_negation = any(word in lower_msg for word in ["didn't", "don't", "no", "not", "never", "haven't"])
        
        # Update activity facts
        if "code" in lower_msg or "coding" in lower_msg or "program" in lower_msg:
            if has_negation:
                self.coded_today = False
                self.invalidated_facts.add("coded_today")
            else:
                self.coded_today = True
                self.invalidated_facts.discard("coded_today")
        
        if "gym" in lower_msg or "workout" in lower_msg or "exercise" in lower_msg:
            if has_negation:
                self.went_gym = False
                self.invalidated_facts.add("went_gym")
            else:
                self.went_gym = True
                self.invalidated_facts.discard("went_gym")
        
        if "study" in lower_msg or "studying" in lower_msg or "learn" in lower_msg:
            if has_negation:
                self.studied_today = False
                self.invalidated_facts.add("studied_today")
            else:
                self.studied_today = True
                self.invalidated_facts.discard("studied_today")
        
        if "cook" in lower_msg or "cooking" in lower_msg or "recipe" in lower_msg:
            if has_negation:
                self.cooked_today = False
                self.invalidated_facts.add("cooked_today")
            else:
                self.cooked_today = True
                self.invalidated_facts.discard("cooked_today")
        
        # Track questions asked by user
        if "?" in message:
            self.user_question_count += 1
        
        # Extract and store specific facts
        self._extract_facts(message)
    
    def _extract_facts(self, message: str):
        """Extract specific facts mentioned in the message."""
        # Example patterns for fact extraction
        patterns = {
            "name": r"(?:i'm|i am|call me|name is)\s+([a-zA-Z]+)",
            "age": r"(?:i'm|i am)\s+(\d+)\s+(?:years? old|y\/o)?",
            "location": r"(?:i live in|i'm from|from)\s+([a-zA-Z\s]+)",
            "project": r"(?:working on|building|making)\s+(.+?)(?:\.|,|$)",
        }
        
        for fact_type, pattern in patterns.items():
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                self.mentioned_facts[fact_type] = match.group(1).strip()
    
    def is_fact_invalidated(self, fact: str) -> bool:
        """Check if a fact has been invalidated in the current conversation."""
        return fact in self.invalidated_facts
    
    def get_context_string(self) -> str:
        """Generate a context string for the LLM prompt."""
        context_parts = []
        
        if self.coded_today is not None:
            context_parts.append(f"User coded today: {self.coded_today}")
        
        if self.went_gym is not None:
            context_parts.append(f"User went to gym today: {self.went_gym}")
        
        if self.studied_today is not None:
            context_parts.append(f"User studied today: {self.studied_today}")
        
        if self.cooked_today is not None:
            context_parts.append(f"User cooked today: {self.cooked_today}")
        
        if self.current_activity:
            context_parts.append(f"Current activity: {self.current_activity}")
        
        if self.current_topic:
            context_parts.append(f"Current topic: {self.current_topic}")
        
        if self.previous_topic:
            context_parts.append(f"Previous topic: {self.previous_topic}")
        
        for fact_type, value in self.mentioned_facts.items():
            context_parts.append(f"User's {fact_type}: {value}")
        
        return "\n".join(context_parts) if context_parts else "No specific facts mentioned in this conversation."