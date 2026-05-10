from typing import TYPE_CHECKING
from event import EventType, Event

if TYPE_CHECKING:
    from character import Character

class HealInstanceSingle(Event):

    Healer: "Character"
    Receiver: "Character"
    HealthRecovered: int

    def __init__(self, GeneratedBy: "Character", Receiver: "Character", HealthRecovered: int):
        super().__init__(EventType.HealInstanceSingle, GeneratedBy)

        self.Healer = self.GeneratedBy
        self.Receiver = Receiver
        self.HealthRecovered = HealthRecovered