from dataclasses import dataclass


@dataclass
class BrainState:

    language: str

    emotion: str
    
    topic: str
    
    style: str
    
    relationship: str
    
    energy: str

    intent: str

    style_profile: dict

    reply_length: str

    ask_question: bool

    tease: bool

    use_memory: bool

    end_conversation: bool

    bubble_count: int

    needs_web: bool