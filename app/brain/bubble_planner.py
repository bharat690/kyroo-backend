# app/brain/bubble_planner.py
from dataclasses import dataclass, field
from typing import List
import random


@dataclass
class Bubble:
    content: str
    purpose: str
    delay: float
    length: str


@dataclass
class BubblePlan:
    bubbles: List[Bubble] = field(default_factory=list)
    total_bubbles: int = 0
    has_question: bool = False
    has_memory_callback: bool = False
    has_tease: bool = False


class BubblePlanner:

    DELAY_RANGES = {
        "reaction": (0.8, 1.5),
        "observation": (1.0, 2.0),
        "question": (1.5, 2.5),
        "follow_up": (2.0, 3.0),
        "tease": (1.0, 2.0),
        "memory_callback": (1.5, 2.5),
        "provide_info": (1.0, 2.0),
        "silent_presence": (2.0, 3.0),
        "react_then_observe": (0.8, 1.5),
        "acknowledge": (0.8, 1.2),
    }

    def plan_bubbles(
        self,
        behavior: str,
        bubble_count: int,
        reply_length: str,
        ask_question: bool,
        need_tease: bool,
        need_memory: bool,
        need_follow_up: bool,
        energy_level: str,
    ) -> BubblePlan:
        plan = BubblePlan()
        plan.total_bubbles = bubble_count

        if bubble_count == 1:
            purpose = behavior
            length = self._bubble_length(reply_length, 1, 1)
            delay = random.uniform(*self.DELAY_RANGES.get(purpose, (1.0, 2.0)))
            plan.bubbles.append(Bubble(content="", purpose=purpose, delay=delay, length=length))
        else:
            purposes = self._sequence(behavior, bubble_count, ask_question, need_tease, need_memory, need_follow_up)
            for i, purpose in enumerate(purposes):
                length = self._bubble_length(reply_length, i + 1, bubble_count)
                delay = random.uniform(*self.DELAY_RANGES.get(purpose, (1.0, 2.0)))
                if energy_level == "high":
                    delay *= 0.8
                elif energy_level == "low":
                    delay *= 1.2
                plan.bubbles.append(Bubble(content="", purpose=purpose, delay=delay, length=length))

        plan.has_question = any(b.purpose == "question" for b in plan.bubbles)
        plan.has_memory_callback = any(b.purpose == "memory_callback" for b in plan.bubbles)
        plan.has_tease = any(b.purpose == "tease" for b in plan.bubbles)
        return plan

    def _sequence(self, behavior, count, ask_question, need_tease, need_memory, need_follow_up):
        seq = []

        if behavior == "react_then_observe":
            seq = ["reaction", "observation"]
        elif behavior == "provide_info":
            seq = ["provide_info"]
            for i in range(1, count):
                seq.append("follow_up" if need_follow_up and i == count - 1 else "provide_info")
        elif behavior == "silent_presence":
            seq = ["silent_presence"] * count
        elif behavior == "memory_callback":
            seq.append("memory_callback")
            if need_tease and count > 1:
                seq.append("tease")
            while len(seq) < count:
                seq.append("observation")
        elif behavior == "provide_presence_then_ask":
            # First bubble: presence, second: gentle question
            seq = ["silent_presence", "question"]
        else:
            seq.append(behavior)
            while len(seq) < count:
                if need_tease and "tease" not in seq:
                    seq.append("tease")
                elif need_memory and "memory_callback" not in seq:
                    seq.append("memory_callback")
                else:
                    seq.append(random.choice(["observation", "reaction"]))

        if ask_question and "question" not in seq:
            seq[-1] = "question"

        return seq[:count]

    def _bubble_length(self, reply_length, pos, total):
        if reply_length == "tiny":
            return "tiny"
        if reply_length == "short":
            return "tiny" if (total > 1 and pos == 1) else "short"
        if reply_length == "medium":
            if total == 1:
                return "medium"
            if total == 2:
                return "short" if pos == 1 else "medium"
            return "tiny" if pos == 1 else "short"
        return "short"

    def get_bubble_context(self, plan: BubblePlan) -> str:
        if not plan.bubbles:
            return "Single bubble response."
        parts = [f"Response Structure: {len(plan.bubbles)} bubbles"]
        for i, b in enumerate(plan.bubbles, 1):
            parts.append(f"Bubble {i}: {b.purpose} ({b.length})")
        return "\n".join(parts)