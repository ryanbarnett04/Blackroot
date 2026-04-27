from typing import TYPE_CHECKING

from ability import Ability
from event import Event

if TYPE_CHECKING:
    from ability import Ability

class EventPipeline:

    RegisteredAbilities: list["Ability"]

    def __init__(self):
        self.RegisteredAbilities = []

    def DistributeEvent(self, event: Event):

        for ability in self.RegisteredAbilities:
            ability.Listener(event)