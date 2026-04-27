from typing import TYPE_CHECKING
from event import EventType, Event

if TYPE_CHECKING:
    from character import Character

class BasicAbilityUsed(Event):

    def __init__(self, GeneratedBy: "Character"):
        super().__init__(EventType.BasicAbilityUsed, GeneratedBy)