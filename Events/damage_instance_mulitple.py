from typing import TYPE_CHECKING
from event import EventType, Event

if TYPE_CHECKING:
    from character import Character

class DamageInstanceMultiple(Event):

    Attacker: "Character"
    Receivers: list["Character"]
    DamageDealt: list[int]
    WasCrit: list[bool]

    def __init__(self, GeneratedBy: "Character", Receivers: list["Character"],
                 DamageDealt: list[int], WasCrit: list[bool]):
        super().__init__(EventType.DamageInstanceMultiple, GeneratedBy)

        self.Attacker = self.GeneratedBy
        self.Receivers = Receivers
        self.DamageDealt = DamageDealt
        self.WasCrit = WasCrit