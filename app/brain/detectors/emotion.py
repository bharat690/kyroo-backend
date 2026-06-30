class EmotionDetector:

    @classmethod
    def detect(cls, text: str) -> str:

        text = text.lower()

        if any(x in text for x in [
            "😭", "😢", "cry", "alone", "lonely", "sad"
        ]):
            return "sad"

        if any(x in text for x in [
            "😡", "angry", "mad"
        ]):
            return "angry"

        if any(x in text for x in [
            "😫", "burnout", "tired", "exhausted"
        ]):
            return "burnout"

        if any(x in text for x in [
            "🔥", "💪", "😈", "yay", "letsgo", "lessgo"
        ]):
            return "excited"

        if any(x in text for x in [
            "😰", "anxiety", "panic", "worried", "stress"
        ]):
            return "anxious"

        return "neutral"