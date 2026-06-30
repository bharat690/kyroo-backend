class LanguageDetector:

    HINDI_WORDS = {
        "hai", "ho", "haan", "nahi", "nhi", "kya", "kyu",
        "kaise", "acha", "accha", "yaar", "bhai", "mera",
        "meri", "tera", "teri", "tum", "aap", "kr", "kar",
        "bhot", "bahut", "fir", "phir", "abhi", "kal"
    }

    @classmethod
    def detect(cls, text: str) -> str:

        text = text.lower()

        words = text.split()

        hindi = sum(
            1
            for word in words
            if word in cls.HINDI_WORDS
        )

        if hindi == 0:
            return "english"

        if hindi >= len(words) * 0.4:
            return "hinglish"

        return "english"