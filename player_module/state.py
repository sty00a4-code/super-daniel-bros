from enum import Enum

class State(Enum):
    Idle = "idle"
    Walk = "walk"
    Jump = "jump"
    Glide = "glide"
    Attack1 = "attack-1"
    Attack2 = "attack-2"
    Attack3 = "attack-3"
    Throw = "throw"
    Pos1 = "pos1"
    Pos2 = "pos2"
    Pos3 = "pos3"