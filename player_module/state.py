from enum import Enum

class State(Enum):
    Idle = "idle"
    Walk = "walk"
    Jump = "jump"
    Glide = "glide"
    Attack = "attack"
    Throw = "throw"