from typing import TYPE_CHECKING
from enum import Enum
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from character import Character
    from event_pipeline import EventPipeline
    from event import Event

class EffectType(Enum):
    Buff = 1
    Debuff = 2
    Neutral = 3

class StatusEffect(ABC):

    Name: str
    Type: EffectType
    Description: str
    Applicant: "Character"
    Duration: int
    Dispellable: bool               # Applicable to Buffs and Debuffs
    Resistable: bool                # Debuffs only - For Buffs set to None
    Preventable: bool               # Buffs only - For Debuffs set to None
    Copyable: bool                  # Buffs only - For Debuffs set to None

    Events: "EventPipeline"

    def __init__(self, Applicant: "Character", Duration: int, Dispellable: bool, Resistable: bool,
                 Preventable: bool, Copyable: bool):
        self.Applicant = Applicant
        self.Duration = Duration
        self.Events = self.Applicant.Events
        self.Dispellable = Dispellable
        self.Resistable = Resistable
        self.Preventable = Preventable
        self.Copyable = Copyable

    @abstractmethod
    def InitialiseEffect(self):
        pass

    @abstractmethod
    def DestroyEffect(self):
        pass

    @abstractmethod
    def Listener(self, event: "Event"):
        pass