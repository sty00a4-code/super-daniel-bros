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
    Dead = "dead"


PLAYER_ATTACK_STATES = [State.Attack1, State.Attack2, State.Attack3]
PLAYER_WALK_IDLE = [State.Idle, State.Walk]
PLAYER_POS_STATES = [State.Pos1, State.Pos2, State.Pos3]
