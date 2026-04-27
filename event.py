from typing import TYPE_CHECKING
from enum import Enum
from abc import ABC

if TYPE_CHECKING:
    from character import Character

class EventType(Enum):
    DamageInstanceSingle = 1
    DamageInstanceMultiple = 2
    HealInstanceSingle = 3
    HealInstanceMultiple = 4
    BuffGained = 5
    DebuffGained = 6
    BuffExpired = 7
    DebuffExpired = 8
    BuffDispelled = 9
    DebuffDispelled = 10
    BasicAbilityUsed = 11
    SpecialAbilityUsed = 12

class Event(ABC):

    Type: EventType

    def __init__(self, Type: EventType, GeneratedBy: "Character"):

        self.Type = Type
        self.GeneratedBy = GeneratedBy