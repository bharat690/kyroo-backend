import re
from typing import List, Dict, Optional

class ResponseValidator:
    """
    Validates and improves AI responses before sending them to the user.
    Checks for various issues and automatically fixes them.
    """
    
    BAD_PHRASES = [
        "it sounds like",
        "i understand",
        "i hear you",
        "maybe you should",
        "it's important",
        "that must be",
        "as an ai",
        "i don't have feelings",
        "i don't have personal",
        "i cannot",
        "i can't",
        "i'm just an ai",
        "as a language model",
        "i'm a language model",
    ]
    
    CORPORATE_WORDING = [
        "leverage",
        "utilize",
        "implement",
        "facilitate",
        "optimize",
        "streamline",
        "synergy",
        "paradigm",
        "incentivize",
        "disrupt",
        "holistic",
        "robust",
        "scalable",
        "actionable",
        "stakeholder",
        "touchpoint",
        "bandwidth",
        "circle back",
        "deep dive",
        "drill down",
        "low-hanging fruit",
        "move the needle",
        "pain point",
        "value proposition",
    ]
    
    AI_SOUNDS = [
        "i'd be happy to",
        "i'd love to",
        "certainly",
        "absolutely",
        "indeed",
        "furthermore",
        "moreover",
        "additionally",
        "consequently",
        "nevertheless",
        "nonetheless",
        "henceforth",
        "thus",
        "therefore",
    ]
    
    MARKDOWN_PATTERNS = [
        r"\*\*.*?\*\*",  # Bold
        r"\*.*?\*",  # Italic
        r"```.*?```",  # Code block
        r"`.*?`",  # Inline code
        r"#{1,6}\s",  # Headers
        r"\[.*?\]\(.*?\)",  # Links
        r"[-*+]\s",  # Unordered lists
        r"\d+\.\s",  # Ordered lists
    ]
    
    MAX_WORDS = 45
    MAX_BUBBLES = 3
    MAX_EMOJIS_PER_BUBBLE = 2
    MAX_QUESTIONS = 1
    
    def validate(
        self,
        response: str,
        plan: Optional[Dict] = None,
    ) -> List[str]:
        """
        Validate and improve a response before sending it.
        
        Args:
            response: The AI's response
            plan: The conversation plan (optional)
            
        Returns:
            List of validated message bubbles
        """
        # Normalize the text
        text = self._normalize(response)
        
        # Remove bad phrases
        text = self._remove_bad_phrases(text)
        
        # Remove corporate wording
        text = self._remove_corporate_wording(text)
        
        # Remove AI-sounding phrases
        text = self._remove_ai_sounds(text)
        
        # Remove markdown formatting
        text = self._remove_markdown(text)
        
        # Split into bubbles
        bubbles = self._split_bubbles(text)
        
        # Validate and improve each bubble
        validated_bubbles = []
        for bubble in bubbles:
            validated_bubble = self._validate_bubble(bubble, plan)
            if validated_bubble:  # Only add non-empty bubbles
                validated_bubbles.append(validated_bubble)
        
        return validated_bubbles[:self.MAX_BUBBLES]  # Limit total bubbles
    
    def _normalize(self, text: str) -> str:
        """Normalize the text format."""
        text = text.replace("\r\n", "\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
    
    def _remove_bad_phrases(self, text: str) -> str:
        """Remove phrases that sound unnatural or AI-like."""
        lower = text.lower()
        
        for phrase in self.BAD_PHRASES:
            if phrase in lower:
                pattern = re.compile(
                    re.escape(phrase),
                    re.IGNORECASE,
                )
                text = pattern.sub("", text)
        
        return text
    
    def _remove_corporate_wording(self, text: str) -> str:
        """Remove corporate-sounding words."""
        lower = text.lower()
        
        for word in self.CORPORATE_WORDING:
            # Use word boundaries to avoid replacing parts of other words
            pattern = re.compile(
                r'\b' + re.escape(word) + r'\b',
                re.IGNORECASE,
            )
            text = pattern.sub("", text)
        
        return text
    
    def _remove_ai_sounds(self, text: str) -> str:
        """Remove phrases that sound too AI-like."""
        lower = text.lower()
        
        for phrase in self.AI_SOUNDS:
            if phrase in lower:
                pattern = re.compile(
                    re.escape(phrase),
                    re.IGNORECASE,
                )
                text = pattern.sub("", text)
        
        return text
    
    def _remove_markdown(self, text: str) -> str:
        """Remove markdown formatting."""
        for pattern in self.MARKDOWN_PATTERNS:
            text = re.sub(pattern, "", text, flags=re.DOTALL)
        
        return text
    
    def _split_bubbles(self, text: str) -> List[str]:
        """Split text into message bubbles."""
        bubbles = [
            bubble.strip()
            for bubble in text.split("\n\n")
            if bubble.strip()
        ]
        
        # If no natural breaks, split by sentences if too long
        if len(bubbles) == 1 and len(bubbles[0].split()) > self.MAX_WORDS:
            sentences = re.split(r'(?<=[.!?])\s+', bubbles[0])
            bubbles = [" ".join(sentences[:2]), " ".join(sentences[2:])]
        
        return bubbles
    
    def _validate_bubble(self, bubble: str, plan: Optional[Dict] = None) -> str:
        """Validate and improve a single message bubble."""
        # Trim words if too long
        bubble = self._trim_words(bubble)
        
        # Limit questions
        bubble = self._limit_questions(bubble)
        
        # Limit emojis
        bubble = self._limit_emojis(bubble, plan)
        
        # Clean up whitespace
        bubble = re.sub(r'\s+', ' ', bubble).strip()
        
        return bubble
    
    def _trim_words(self, text: str) -> str:
        """Trim text to maximum word count."""
        words = text.split()
        if len(words) <= self.MAX_WORDS:
            return text
        
        # Try to cut at a sentence boundary
        trimmed = " ".join(words[:self.MAX_WORDS])
        last_sentence_end = max(trimmed.rfind('.'), trimmed.rfind('!'), trimmed.rfind('?'))
        
        if last_sentence_end > self.MAX_WORDS * 0.7:  # If we can cut at a sentence near the end
            return trimmed[:last_sentence_end+1]
        
        return trimmed
    
    def _limit_questions(self, text: str) -> str:
        """Limit the number of questions in the text."""
        count = 0
        result = []
        
        for char in text:
            if char == "?":
                count += 1
                if count > self.MAX_QUESTIONS:
                    continue
            result.append(char)
        
        return "".join(result)
    
    def _limit_emojis(self, text: str, plan: Optional[Dict] = None) -> str:
        """Limit the number of emojis in the text."""
        # Emoji pattern
        emoji_pattern = re.compile(
            "["
            "\U0001F300-\U0001FAFF"  # Miscellaneous Symbols and Pictographs
            "\U00002700-\U000027BF"  # Dingbats
            "\U0001F600-\U0001F64F"  # Emoticons
            "\U0001F680-\U0001F6FF"  # Transport and Map
            "\U0001F1E0-\U0001F1FF"  # Flags
            "\U00002600-\U000026FF"  # Miscellaneous Symbols
            "\U0000FE00-\U0000FE0F"  # Variation Selectors
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "]",
            flags=re.UNICODE,
        )
        
        # Determine emoji budget from plan or use default
        emoji_budget = self.MAX_EMOJIS_PER_BUBBLE
        if plan and "emoji_budget" in plan:
            try:
                emoji_budget = int(plan["emoji_budget"])
            except (ValueError, TypeError):
                pass
        
        # Find all emojis
        emojis = emoji_pattern.findall(text)
        
        # If within budget, return as is
        if len(emojis) <= emoji_budget:
            return text
        
        # Otherwise, remove exces   s emojis
        result = text
        for _ in range(len(emojis) - emoji_budget):
            result = emoji_pattern.sub("", result, count=1)
        
        return result