import re


class ResponseValidator:

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
    ]

    MAX_WORDS = 45
    MAX_BUBBLES = 3

    def validate(
        self,
        response: str,
    ) -> list[str]:

        text = self._normalize(response)

        text = self._remove_bad_phrases(text)

        text = self._limit_questions(text)

        text = self._trim_words(text)

        bubbles = self._split_bubbles(text)

        return bubbles

    def _normalize(self, text: str) -> str:

        text = text.replace("\r\n", "\n")

        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def _remove_bad_phrases(
        self,
        text: str,
    ) -> str:

        lower = text.lower()

        for phrase in self.BAD_PHRASES:

            if phrase in lower:

                pattern = re.compile(
                    re.escape(phrase),
                    re.IGNORECASE,
                )

                text = pattern.sub("", text)

        return text

    def _limit_questions(
        self,
        text: str,
    ) -> str:

        count = 0

        result = []

        for char in text:

            if char == "?":

                count += 1

                if count > 1:
                    continue

            result.append(char)

        return "".join(result)

    def _trim_words(
        self,
        text: str,
    ) -> str:

        words = text.split()

        if len(words) <= self.MAX_WORDS:
            return text

        return " ".join(words[: self.MAX_WORDS])

    def _split_bubbles(
        self,
        text: str,
    ) -> list[str]:

        bubbles = [
            bubble.strip()
            for bubble in text.split("\n\n")
            if bubble.strip()
        ]

        return bubbles[: self.MAX_BUBBLES]