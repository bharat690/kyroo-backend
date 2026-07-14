from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
import re

@dataclass
class Topic:
    """Represents a conversation topic."""
    name: str
    keywords: List[str]
    start_message_index: int
    end_message_index: Optional[int] = None
    is_active: bool = True
    subtopics: List[str] = field(default_factory=list)

class TopicTracker:
    """
    Tracks conversation topics and their evolution.
    """
    
    # Define topic categories and their keywords
    TOPIC_CATEGORIES: Dict[str, List[str]] = {
        "general": [],
        "fitness": ["gym", "workout", "exercise", "fitness", "protein", "cardio", "muscle", "weight", "diet"],
        "study": ["study", "learn", "exam", "course", "lecture", "homework", "assignment", "thesis", "research"],
        "coding": ["code", "coding", "programming", "debug", "develop", "software", "app", "website", "api"],
        "cooking": ["cook", "recipe", "food", "meal", "kitchen", "ingredient", "bake", "grill", "dish"],
        "entertainment": ["movie", "show", "series", "music", "game", "anime", "netflix", "spotify", "song"],
        "finance": ["money", "expense", "budget", "investment", "salary", "savings", "stock", "crypto"],
        "travel": ["travel", "trip", "vacation", "flight", "hotel", "destination", "visit", "tourist"],
        "health": ["health", "doctor", "medicine", "symptom", "diet", "sleep", "mental health", "wellness"],
        "work": ["work", "office", "meeting", "project", "deadline", "colleague", "boss", "job", "company"],
        "relationships": ["friend", "family", "relationship", "dating", "partner", "love", "boyfriend", "girlfriend"],
        "technology": ["phone", "laptop", "computer", "gadget", "tech", "device", "software", "hardware"],
    }
    
    def __init__(self):
        self.topics: List[Topic] = []
        self.current_topic: Optional[Topic] = None
        self.resolved_topics: List[Topic] = []
        self.message_index = 0
    
    def update(self, message: str) -> str:
        """
        Update topic tracking with a new message.
        
        Args:
            message: The user's message
            
        Returns:
            The current topic name
        """
        self.message_index += 1
        detected_topic = self._detect_topic(message)
        
        # If no topic detected, keep the current topic
        if detected_topic == "general" and self.current_topic:
            return self.current_topic.name
        
        # If topic changed, handle the transition
        if self.current_topic and detected_topic != self.current_topic.name:
            self._handle_topic_change(detected_topic)
        
        # If it's a new topic, create a new Topic object
        if not self.current_topic or detected_topic != self.current_topic.name:
            keywords = self._extract_topic_keywords(message, detected_topic)
            self.current_topic = Topic(
                name=detected_topic,
                keywords=keywords,
                start_message_index=self.message_index
            )
            self.topics.append(self.current_topic)
        
        # Update subtopics if applicable
        self._update_subtopics(message)
        
        return detected_topic
    
    def _detect_topic(self, message: str) -> str:
        """Detect the topic of a message."""
        message_lower = message.lower()
        
        # Score each topic category
        topic_scores = {}
        
        for topic, keywords in self.TOPIC_CATEGORIES.items():
            if topic == "general":
                continue
                
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                topic_scores[topic] = score / len(keywords)
        
        # If no topic detected, return general
        if not topic_scores:
            return "general"
        
        # Return the topic with the highest score
        return max(topic_scores.items(), key=lambda x: x[1])[0]
    
    def _extract_topic_keywords(self, message: str, topic: str) -> List[str]:
        """Extract relevant keywords from the message for the given topic."""
        if topic == "general":
            return []
        
        topic_keywords = self.TOPIC_CATEGORIES.get(topic, [])
        message_words = re.findall(r'\b\w+\b', message.lower())
        
        # Return keywords that are in both the message and the topic's keyword list
        return [word for word in message_words if word in topic_keywords]
    
    def _handle_topic_change(self, new_topic: str):
        """Handle a change in topic."""
        if self.current_topic:
            # Mark the previous topic as inactive
            self.current_topic.is_active = False
            self.current_topic.end_message_index = self.message_index - 1
            
            # Add to resolved topics if it's not too short
            if self.message_index - self.current_topic.start_message_index >= 3:
                self.resolved_topics.append(self.current_topic)
    
    def _update_subtopics(self, message: str):
        """Update subtopics for the current topic."""
        if not self.current_topic or self.current_topic.name == "general":
            return
        
        # Extract potential subtopics (this is a simple implementation)
        # In a more sophisticated system, this could use NLP techniques
        words = re.findall(r'\b\w+\b', message.lower())
        
        # Filter out common words and keep only potential subtopics
        common_words = {"i", "me", "my", "we", "our", "you", "your", "is", "am", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "shall", "should", "may", "might", "must", "can", "could", "a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet", "at", "by", "from", "in", "into", "of", "on", "to", "with"}
        
        potential_subtopics = [word for word in words if word not in common_words and len(word) > 3]
        
        # Add unique subtopics
        for subtopic in potential_subtopics:
            if subtopic not in self.current_topic.subtopics:
                self.current_topic.subtopics.append(subtopic)
    
    def get_topic_context(self) -> str:
        """
        Get a context string about the current topic state for the LLM prompt.
        
        Returns:
            A string describing the current topic state
        """
        context_parts = []
        
        if self.current_topic:
            context_parts.append(f"Current Topic: {self.current_topic.name}")
            
            if self.current_topic.subtopics:
                context_parts.append(f"Subtopics: {', '.join(self.current_topic.subtopics[:5])}")  # Limit to 5 subtopics
        
        if self.resolved_topics:
            # Get the last few resolved topics
            recent_resolved = self.resolved_topics[-3:]  # Limit to 3 most recent
            resolved_names = [topic.name for topic in recent_resolved]
            context_parts.append(f"Recently Discussed: {', '.join(resolved_names)}")
        
        return "\n".join(context_parts) if context_parts else "No specific topic detected."