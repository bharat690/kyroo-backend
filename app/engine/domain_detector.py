class DomainDetector:

    KEYWORDS = {
        "fitness": [
            "gym",
            "protein",
            "workout",
            "exercise",
            "weight",
        ],
        "finance": [
            "money",
            "expense",
            "salary",
            "upi",
        ],
        "sleep": [
            "sleep",
            "nap",
            "awake",
        ],
        "goals": [
            "goal",
            "habit",
            "todo",
        ],
    }

    def detect(self, message: str) -> str:

        text = message.lower()

        for domain, words in self.KEYWORDS.items():

            if any(word in text for word in words):
                return domain

        return "general"