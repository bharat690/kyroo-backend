import re

CLICHE_PHRASES = [
    "i understand", "i cannot", "as an ai", "certainly!", "of course!",
    "great question!", "it sounds like", "i'm sorry to hear", "i apologize",
    "as a language model", "i'm just an ai", "i don't have the ability to",
]

MAX_REPLY_WORDS = 60
MAX_REPLY_WORDS_LIST = 500

_LIST_LINE = re.compile(r'^\s*(\d+[.)]|[-•*])\s', re.MULTILINE)

# Safety net for leaked internal reasoning/meta-commentary (the model
# narrating its own instruction-following instead of just replying).
_LEAK_SIGNATURES = [
    "the instructions", "the system prompt", "staying in character",
    "i need to continue the conversation", "i need to re-read",
    "let me re-read", "let me check what i'm doing", "what i'm doing wrong",
    "staying in character as kyroo", "i'm doing wrong", "core personality rules",
    "user just said", "user just sent", "in response to my latest message",
]


def _is_leaked_reasoning(bubble: str) -> bool:
    low = bubble.lower()
    return any(sig in low for sig in _LEAK_SIGNATURES)


_EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F9FF"
    "\U00002702-\U000027B0"
    "\U0001FA00-\U0001FAFF"
    "]",
    flags=re.UNICODE,
)

MAX_EMOJIS_PER_BUBBLE = 1


def _cap_emojis(bubble: str, max_emojis: int = MAX_EMOJIS_PER_BUBBLE) -> str:
    """Hard backstop for the 'strict max 1 emoji per message' persona rule —
    the model doesn't always follow it, so enforce it in code too."""
    matches = list(_EMOJI_PATTERN.finditer(bubble))
    if len(matches) <= max_emojis:
        return bubble
    keep = {m.start() for m in matches[:max_emojis]}
    chars = [c for i, c in enumerate(bubble) if not (_EMOJI_PATTERN.match(c) and i not in keep)]
    return re.sub(r' {2,}', ' ', "".join(chars)).strip()


def validate_response(text: str) -> list[str]:
    """Validate and split a raw model reply into WhatsApp-ready bubbles."""
    cleaned = text.strip()

    for phrase in CLICHE_PHRASES:
        cleaned = re.sub(re.escape(phrase), "", cleaned, flags=re.IGNORECASE)

    cleaned = re.sub(r' {2,}', ' ', cleaned)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned).strip()

    is_list = len(_LIST_LINE.findall(cleaned)) >= 2

    if not is_list:
        q_positions = [i for i, c in enumerate(cleaned) if c == '?']
        if len(q_positions) > 1:
            chars = list(cleaned)
            for i in q_positions[1:]:
                chars[i] = '.'
            cleaned = "".join(chars)

    word_limit = MAX_REPLY_WORDS_LIST if is_list else MAX_REPLY_WORDS
    words = cleaned.split()
    if len(words) > word_limit:
        hard_cut = " ".join(words[:word_limit])
        last_sentence_end = max(hard_cut.rfind("."), hard_cut.rfind("!"), hard_cut.rfind("?"))
        # prefer cutting at a sentence boundary if it doesn't lose too much content
        if last_sentence_end > len(hard_cut) * 0.4:
            cleaned = hard_cut[:last_sentence_end + 1]
        else:
            cleaned = hard_cut

    bubbles = [b.strip() for b in cleaned.split("\n\n") if b.strip()]
    bubbles = [b for b in bubbles if not _is_leaked_reasoning(b)]
    bubbles = [_cap_emojis(b) for b in bubbles]
    if not bubbles:
        bubbles = ["hmm one sec, my brain glitched, say that again?"]
    return bubbles[:4]
