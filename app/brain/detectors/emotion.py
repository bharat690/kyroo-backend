import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class EmotionResult:
    """Result of emotion detection."""
    emotion: str
    intensity: float  # 0.0 to 1.0
    keywords: List[str]  # Keywords that triggered this emotion

class EmotionDetector:
    """
    Detects emotions in user messages with more granularity.
    """
    
    EMOTION_PATTERNS: Dict[str, List[str]] = {
        "sad": ["😭", "😢", "cry", "alone", "lonely", "sad", "depressed", "down", "upset", "heartbroken", "miss"],
        "burnout": ["😫", "burnout", "tired", "exhausted", "drained", "overwhelmed", "stressed out", "can't do this"],
        "angry": ["😡", "😤", "angry", "mad", "furious", "pissed", "annoyed", "frustrated", "hate"],
        "confused": ["🤔", "confused", "don't understand", "what do you mean", "huh", "lost", "unclear"],
        "excited": ["🔥", "💪", "😈", "yay", "letsgo", "lessgo", "excited", "awesome", "amazing", "can't wait", "pumped"],
        "proud": ["🥳", "proud", "accomplished", "did it", "nailed it", "achieved", "success"],
        "embarrassed": ["😅", "embarrassed", "awkward", "cringe", "shy", "bashful"],
        "anxious": ["😰", "anxiety", "panic", "worried", "stress", "nervous", "scared", "fear"],
        "bored": ["😴", "bored", "boring", "nothing to do", "boredom"],
        "sarcastic": ["🙄", "sure", "obviously", "right", "yeah right", "as if", "whatever"],
        "happy": ["😊", "😀", "happy", "glad", "joy", "great", "good", "nice", "wonderful", "fantastic"],
        "grateful": ["🙏", "thank", "thanks", "grateful", "appreciate"],
        "nostalgic": ["🥺", "remember when", "miss those days", "nostalgia", "good old days"],
    }
    
    # Emotion modifiers that increase intensity
    INTENSITY_MODIFIERS = {
        "very": 1.2,
        "really": 1.3,
        "so": 1.2,
        "extremely": 1.4,
        "incredibly": 1.4,
        "super": 1.3,
        "a bit": 0.7,
        "slightly": 0.7,
        "kind of": 0.8,
        "somewhat": 0.8,
    }
    
    @classmethod
    def detect(cls, text: str) -> str:
        """Detect the primary emotion in the text."""
        result = cls.detect_detailed(text)
        return result.emotion
    
    @classmethod
    def detect_detailed(cls, text: str) -> EmotionResult:
        """
        Detect emotion with detailed information including intensity and keywords.
        
        Args:
            text: The user's message
            
        Returns:
            EmotionResult with emotion, intensity, and triggering keywords
        """
        text_lower = text.lower()
        
        # Calculate base intensity from modifiers
        base_intensity = 1.0
        for modifier, multiplier in cls.INTENSITY_MODIFIERS.items():
            if modifier in text_lower:
                base_intensity = multiplier
                break
        
        # Score each emotion
        emotion_scores = {}
        emotion_keywords = {}
        
        for emotion, patterns in cls.EMOTION_PATTERNS.items():
            matching_keywords = [pattern for pattern in patterns if pattern in text_lower]
            if matching_keywords:
                # Base score is the proportion of matching patterns
                score = len(matching_keywords) / len(patterns)
                # Adjust by intensity modifiers
                score *= base_intensity
                emotion_scores[emotion] = score
                emotion_keywords[emotion] = matching_keywords
        
        # If no emotion detected, return neutral
        if not emotion_scores:
            return EmotionResult(
                emotion="neutral",
                intensity=0.0,
                keywords=[]
            )
        
        # Get the highest scoring emotion
        best_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        
        # Calculate intensity (0.0 to 1.0)
        intensity = min(1.0, best_emotion[1])
        
        return EmotionResult(
            emotion=best_emotion[0],
            intensity=intensity,
            keywords=emotion_keywords[best_emotion[0]]
        )
    
    @classmethod
    def get_emotion_response_guidelines(cls, emotion: str) -> Dict[str, str]:
        """
        Get guidelines for responding to a specific emotion.
        
        Args:
            emotion: The detected emotion
            
        Returns:
            Dictionary with response guidelines
        """
        guidelines = {
            "energy": "medium",
            "questions": "optional",
            "reply_length": "short",
            "teasing": "allowed",
            "emoji_budget": "1",
            "approach": "normal"
        }
        
        if emotion == "sad":
            guidelines.update({
                "energy": "low",
                "questions": "gentle",
                "reply_length": "medium",
                "teasing": "avoid",
                "emoji_budget": "0",
                "approach": "comfort first"
            })
        
        elif emotion == "burnout":
            guidelines.update({
                "energy": "low",
                "questions": "avoid",
                "reply_length": "medium",
                "teasing": "avoid",
                "emoji_budget": "0",
                "approach": "validate first"
            })
        
        elif emotion == "angry":
            guidelines.update({
                "energy": "low",
                "questions": "avoid",
                "reply_length": "short",
                "teasing": "avoid",
                "emoji_budget": "0",
                "approach": "stay calm"
            })
        
        elif emotion == "excited":
            guidelines.update({
                "energy": "high",
                "questions": "optional",
                "reply_length": "short",
                "teasing": "allowed",
                "emoji_budget": "2",
                "approach": "match excitement"
            })
        
        elif emotion == "proud":
            guidelines.update({
                "energy": "high",
                "questions": "optional",
                "reply_length": "short",
                "teasing": "playful",
                "emoji_budget": "1",
                "approach": "celebrate harder"
            })
        
        elif emotion == "anxious":
            guidelines.update({
                "energy": "low",
                "questions": "gentle",
                "reply_length": "medium",
                "teasing": "avoid",
                "emoji_budget": "0",
                "approach": "slow the conversation"
            })
        
        elif emotion == "bored":
            guidelines.update({
                "energy": "medium",
                "questions": "suggest",
                "reply_length": "short",
                "teasing": "playful",
                "emoji_budget": "0",
                "approach": "offer suggestions"
            })
        
        elif emotion == "sarcastic":
            guidelines.update({
                "energy": "medium",
                "questions": "avoid",
                "reply_length": "short",
                "teasing": "match",
                "emoji_budget": "1",
                "approach": "play along"
            })
        
        return guidelines