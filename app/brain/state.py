from dataclasses import dataclass


@dataclass
class BrainState:

    language: str

    emotion: str

    topic: str

    style: str

    relationship: str

    energy: str