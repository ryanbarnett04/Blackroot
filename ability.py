from abc import ABC, abstractmethod
from enum import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from character import Character
    from event import Event

class AbilityType(Enum):
    Basic = 1
    Special = 2
    Leader = 3
    Unique = 4
    Granted = 5

class Ability(ABC):

    Name: str
    Type: AbilityType
    Cooldown: int           # None if no cooldown
    TurnsToNextUse: int     # None if no cooldown

    def __init__(self, User: "Character", Name: str, Type: AbilityType, Cooldown, TurnsToNextUse):

        self.User = User
        self.Name = Name
        self.Type = Type
        self.Cooldown = Cooldown
        self.TurnsToNextUse = TurnsToNextUse

    def GetName(self):
        return self.Name

    def GetType(self):
        return self.Type

    def ModifyCooldown(self, modifier: int):
        self.Cooldown = self.Cooldown + modifier

    def GetCooldown(self):
        return self.Cooldown

    def ModifyTurnsToNextUse(self, modifier: int):
        self.TurnsToNextUse = self.TurnsToNextUse + modifier

    @abstractmethod
    def Activate(self, Allies: list["Character"], Enemies: list["Character"], TargetEnemyIndex: int, TargetAllyIndex: int):
        pass

    @abstractmethod
    def Listener(self, event: "Event"):
        pass