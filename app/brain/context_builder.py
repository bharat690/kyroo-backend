from app.brain.detectors.emotion import EmotionDetector
from app.brain.detectors.language import LanguageDetector
from app.brain.state import BrainState


class ContextBuilder:

    def build(
        self,
        message: str,
    ) -> BrainState:

        language = LanguageDetector.detect(message)

        emotion = EmotionDetector.detect(message)

        return BrainState(
            language=language,
            emotion=emotion,
            topic="general",
            style="casual",
            relationship="returning_user",
            energy="medium",
        )