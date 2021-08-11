from enum import Enum, unique


@unique
class RotStates(Enum):
    YES = "yes"
    NO = "no"
    MAYBE = "maybe"
