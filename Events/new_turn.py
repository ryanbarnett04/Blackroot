from typing import TYPE_CHECKING
from event import EventType, Event

if TYPE_CHECKING:
    from character import Character

class NewTurn(Event):

    def __init__(self, GeneratedBy: "Character"):
        super().__init__(EventType.NewTurn, GeneratedBy)
        self.InTurn = GeneratedBy