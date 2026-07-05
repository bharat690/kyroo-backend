import re


class StyleLearner:

    EMOJIS = re.compile(
        "["
        "\U0001F300-\U0001FAFF"
        "\U00002700-\U000027BF"
        "]",
        flags=re.UNICODE,
    )

    GENZ = {
        "bro", "fr", "ngl", "lowkey", "highkey",
        "slay", "bestie", "period", "cook", "cooked",
        "lmao", "lol", "tf", "idk", "sus",
        "mid", "aura", "rizz", "bet"
    }

    HINGLISH = {
        "hai", "ho", "kya", "yaar", "bhai",
        "nahi", "acha", "accha", "kar",
        "kr", "mera", "teri", "tum"
    }

    @classmethod
    def learn(cls, history):

        if not history:

            return {
                "emoji_rate": "low",
                "reply_style": "short",
                "capitalization": "lower",
                "genz": False,
                "hinglish": False,
            }

        total_words = 0
        emoji_count = 0
        upper = 0
        lower = 0
        genz = 0
        hinglish = 0

        for msg in history:

            text = msg.content

            total_words += len(text.split())

            emoji_count += len(cls.EMOJIS.findall(text))

            upper += sum(c.isupper() for c in text)

            lower += sum(c.islower() for c in text)

            words = text.lower().split()

            genz += sum(w in cls.GENZ for w in words)

            hinglish += sum(w in cls.HINGLISH for w in words)

        avg_words = total_words / len(history)

        if avg_words < 6:
            reply_style = "tiny"
        elif avg_words < 15:
            reply_style = "short"
        else:
            reply_style = "medium"

        emoji_rate = "low"

        if emoji_count > len(history):
            emoji_rate = "medium"

        if emoji_count > len(history) * 2:
            emoji_rate = "high"

        capitalization = "lower"

        if upper > lower * 0.15:
            capitalization = "mixed"

        return {
            "emoji_rate": emoji_rate,
            "reply_style": reply_style,
            "capitalization": capitalization,
            "genz": genz > 3,
            "hinglish": hinglish > 3,
        }