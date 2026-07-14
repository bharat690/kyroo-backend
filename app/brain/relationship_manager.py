from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class RelationshipLevel(Enum):
    NEW_USER = "new_user"
    RETURNING = "returning"
    REGULAR = "regular"
    FRIEND = "friend"
    CLOSE_FRIEND = "close_friend"

@dataclass
class RelationshipProfile:
    """Profile tracking the relationship between the user and Kyroo."""
    level: RelationshipLevel = RelationshipLevel.NEW_USER
    total_conversations: int = 0
    total_messages: int = 0
    days_since_first_interaction: int = 0
    days_since_last_interaction: int = 0
    avg_messages_per_conversation: float = 0.0
    user_initiated_percentage: float = 0.0
    emotional_sharing_count: int = 0
    personal_info_shared: List[str] = field(default_factory=list)
    inside_jokes: List[str] = field(default_factory=list)
    preferences: Dict[str, str] = field(default_factory=dict)
    interaction_quality_scores: List[float] = field(default_factory=list)

class RelationshipManager:
    """
    Manages and tracks the relationship between the user and Kyroo.
    Determines the appropriate relationship level and adjusts interaction style.
    """
    
    # Thresholds for relationship level upgrades
    LEVEL_THRESHOLDS = {
        RelationshipLevel.NEW_USER: {
            "min_conversations": 0,
            "min_messages": 0,
            "min_days": 0,
        },
        RelationshipLevel.RETURNING: {
            "min_conversations": 2,
            "min_messages": 10,
            "min_days": 1,
        },
        RelationshipLevel.REGULAR: {
            "min_conversations": 10,
            "min_messages": 100,
            "min_days": 7,
        },
        RelationshipLevel.FRIEND: {
            "min_conversations": 30,
            "min_messages": 300,
            "min_days": 30,
        },
        RelationshipLevel.CLOSE_FRIEND: {
            "min_conversations": 100,
            "min_messages": 1000,
            "min_days": 90,
        },
    }
    
    # Relationship level modifiers
    LEVEL_MODIFIERS = {
        RelationshipLevel.NEW_USER: {
            "teasing": False,
            "nicknames": False,
            "memory_usage": "minimal",
            "warmth": "neutral",
            "conversation_depth": "surface",
            "emoji_usage": "minimal",
        },
        RelationshipLevel.RETURNING: {
            "teasing": False,
            "nicknames": False,
            "memory_usage": "basic",
            "warmth": "friendly",
            "conversation_depth": "surface",
            "emoji_usage": "normal",
        },
        RelationshipLevel.REGULAR: {
            "teasing": "light",
            "nicknames": False,
            "memory_usage": "moderate",
            "warmth": "warm",
            "conversation_depth": "moderate",
            "emoji_usage": "normal",
        },
        RelationshipLevel.FRIEND: {
            "teasing": "moderate",
            "nicknames": "occasional",
            "memory_usage": "extensive",
            "warmth": "very_warm",
            "conversation_depth": "deep",
            "emoji_usage": "frequent",
        },
        RelationshipLevel.CLOSE_FRIEND: {
            "teasing": "frequent",
            "nicknames": "regular",
            "memory_usage": "extensive",
            "warmth": "very_warm",
            "conversation_depth": "very_deep",
            "emoji_usage": "frequent",
        },
    }
    
    @classmethod
    def update_relationship(cls, profile: RelationshipProfile, user_id: str, db) -> RelationshipProfile:
        """
        Update the relationship profile based on interaction history.
        
        Args:
            profile: Current relationship profile
            user_id: User ID
            db: Database session
            
        Returns:
            Updated relationship profile
        """
        # In a real implementation, this would query the database for interaction history
        # For now, we'll simulate the update based on the profile data
        
        # Update relationship level based on thresholds
        profile.level = cls._determine_relationship_level(profile)
        
        return profile
    
    @classmethod
    def _determine_relationship_level(cls, profile: RelationshipProfile) -> RelationshipLevel:
        """Determine the appropriate relationship level based on the profile."""
        # Check each level from highest to lowest
        for level in reversed(list(RelationshipLevel)):
            thresholds = cls.LEVEL_THRESHOLDS[level]
            
            if (profile.total_conversations >= thresholds["min_conversations"] and
                profile.total_messages >= thresholds["min_messages"] and
                profile.days_since_first_interaction >= thresholds["min_days"]):
                return level
        
        return RelationshipLevel.NEW_USER
    
    @classmethod
    def get_relationship_modifiers(cls, level: RelationshipLevel) -> Dict:
        """
        Get interaction modifiers based on the relationship level.
        
        Args:
            level: Current relationship level
            
        Returns:
            Dictionary of interaction modifiers
        """
        return cls.LEVEL_MODIFIERS.get(level, cls.LEVEL_MODIFIERS[RelationshipLevel.NEW_USER])
    
    @classmethod
    def get_relationship_context(cls, profile: RelationshipProfile) -> str:
        """
        Get a context string about the relationship for the LLM prompt.
        
        Args:
            profile: Current relationship profile
            
        Returns:
            A string describing the relationship context
        """
        level = profile.level
        modifiers = cls.get_relationship_modifiers(level)
        
        context_parts = [
            f"Relationship Level: {level.value}",
            f"Teasing: {modifiers['teasing']}",
            f"Use Nicknames: {modifiers['nicknames']}",
            f"Memory Usage: {modifiers['memory_usage']}",
            f"Warmth Level: {modifiers['warmth']}",
            f"Conversation Depth: {modifiers['conversation_depth']}",
            f"Emoji Usage: {modifiers['emoji_usage']}",
        ]
        
        if profile.inside_jokes:
            context_parts.append(f"Inside Jokes: {', '.join(profile.inside_jokes[:3])}")  # Limit to 3 jokes
        
        return "\n".join(context_parts)
    
    @classmethod
    def record_interaction(cls, profile: RelationshipProfile, was_user_initiated: bool, had_emotional_content: bool) -> RelationshipProfile:
        """
        Record a new interaction and update the profile.
        
        Args:
            profile: Current relationship profile
            was_user_initiated: Whether the user initiated the conversation
            had_emotional_content: Whether the conversation had emotional content
            
        Returns:
            Updated relationship profile
        """
        profile.total_messages += 1
        
        if was_user_initiated:
            # Simple moving average for user initiation percentage
            if profile.total_messages == 1:
                profile.user_initiated_percentage = 100.0
            else:
                profile.user_initiated_percentage = (
                    (profile.user_initiated_percentage * (profile.total_messages - 1) + 100) / 
                    profile.total_messages
                )
        else:
            if profile.total_messages == 1:
                profile.user_initiated_percentage = 0.0
            else:
                profile.user_initiated_percentage = (
                    profile.user_initiated_percentage * (profile.total_messages - 1) / 
                    profile.total_messages
                )
        
        if had_emotional_content:
            profile.emotional_sharing_count += 1
        
        return profile
    
    @classmethod
    def add_inside_joke(cls, profile: RelationshipProfile, joke: str) -> RelationshipProfile:
        """Add an inside joke to the profile."""
        if joke not in profile.inside_jokes and len(profile.inside_jokes) < 10:  # Limit to 10 jokes
            profile.inside_jokes.append(joke)
        return profile
    
    @classmethod
    def add_personal_info(cls, profile: RelationshipProfile, info_type: str, info_value: str) -> RelationshipProfile:
        """Add personal information to the profile."""
        key = f"{info_type}:{info_value}"
        if key not in profile.personal_info_shared:
            profile.personal_info_shared.append(key)
        return profile
    
    @classmethod
    def update_preference(cls, profile: RelationshipProfile, preference_type: str, preference_value: str) -> RelationshipProfile:
        """Update a user preference in the profile."""
        profile.preferences[preference_type] = preference_value
        return profile