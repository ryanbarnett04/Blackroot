from typing import TYPE_CHECKING
from event import EventType, Event

if TYPE_CHECKING:
    from character import Character

class BuffGained(Event):

    GrantedBy: "Character"
    GrantedTo: "Character"
    BuffGranted: str
    Duration: int

    def __init__(self, GeneratedBy: "Character", GrantedTo: "Character", BuffGranted: str,
                 Duration: int):
        super().__init__(EventType.BuffGained, GeneratedBy)

        self.GrantedBy = self.GeneratedBy
        self.GrantedTo = GrantedTo
        self.BuffGranted = BuffGranted
        self.Duration = Duration