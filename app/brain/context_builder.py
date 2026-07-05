from app.brain.detectors.emotion import EmotionDetector
from app.brain.detectors.language import LanguageDetector
from app.brain.state import BrainState


class ContextBuilder:

    GREETINGS = {
        "hi",
        "hii",
        "hiii",
        "hello",
        "hey",
        "heyy",
        "yo",
        "sup",
    }

    FITNESS = {
        "gym",
        "workout",
        "exercise",
        "pushup",
        "fitness",
        "protein",
        "cardio",
    }

    STUDY = {
        "study",
        "machine learning",
        "ml",
        "ai",
        "python",
        "coding",
        "leetcode",
        "gate",
        "project",
        "exam",
    }

    COOKING = {
        "recipe",
        "cook",
        "food",
        "meal",
        "kitchen",
    }

    def build(
        self,
        message: str,
    ) -> BrainState:

        msg = message.lower()

        language = LanguageDetector.detect(message)

        emotion = EmotionDetector.detect(message)

        intent = "casual"

        topic = "general"

        needs_web = False

        tease = False

        ask_question = False

        use_memory = True

        end_conversation = False

        bubble_count = 2

        reply_length = "short"

        # Greeting

        if msg.strip() in self.GREETINGS:

            intent = "greeting"

            ask_question = False

            use_memory = False

            end_conversation = True

            bubble_count = 1

            reply_length = "tiny"

        # Fitness

        elif any(word in msg for word in self.FITNESS):

            intent = "fitness"

            topic = "fitness"

            tease = True

            ask_question = False

        # Study

        elif any(word in msg for word in self.STUDY):

            intent = "study"

            topic = "study"

            tease = False

            ask_question = True

        # Cooking

        elif any(word in msg for word in self.COOKING):

            intent = "cooking"

            topic = "cooking"

            ask_question = False

        # Resource Requests

        if any(word in msg for word in [
            "best",
            "latest",
            "tutorial",
            "course",
            "youtube",
            "github",
            "resources",
            "documentation",
        ]):

            needs_web = True

        # Emotional

        if emotion != "neutral":

            ask_question = True

            tease = False

            bubble_count = 2

            reply_length = "medium"

        return BrainState(
            language=language,
            emotion=emotion,
            topic=topic,
            style="casual",
            relationship="returning_user",
            energy="medium",
            intent=intent,
            reply_length=reply_length,
            ask_question=ask_question,
            tease=tease,
            use_memory=use_memory,
            end_conversation=end_conversation,
            bubble_count=bubble_count,
            needs_web=needs_web,
        )