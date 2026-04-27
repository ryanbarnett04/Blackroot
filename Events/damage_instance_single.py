from typing import TYPE_CHECKING
from event import EventType, Event

if TYPE_CHECKING:
    from character import Character

class DamageInstanceSingle(Event):

    Attacker: "Character"
    Receiver: "Character"
    DamageDealt: int
    WasCrit: bool

    def __init__(self, GeneratedBy: "Character", Receiver: "Character", DamageDealt: int,
                 WasCrit: bool):
        super().__init__(EventType.DamageInstanceSingle, GeneratedBy)

        self.Attacker = self.GeneratedBy
        self.Receiver = Receiver
        self.DamageDealt = DamageDealt
        self.WasCrit = WasCrit