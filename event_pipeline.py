from typing import TYPE_CHECKING

from ability import Ability
from event import Event

if TYPE_CHECKING:
    from ability import Ability
    from status_effect import StatusEffect

class EventPipeline:

    RegisteredAbilities: list["Ability"]
    RegisteredEffects: list["StatusEffect"]

    def __init__(self):
        self.RegisteredAbilities = []
        self.RegisteredEffects = []

    def DistributeEvent(self, event: Event):

        for ability in self.RegisteredAbilities:
            ability.Listener(event)

        for effect in self.RegisteredEffects:
            effect.Listener(event)