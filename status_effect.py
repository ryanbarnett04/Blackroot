from typing import TYPE_CHECKING
from enum import Enum
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from character import Character
    from event_pipeline import EventPipeline

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
    Events: "EventPipeline"

    def __init__(self, Applicant: "Character", Duration: int):
        self.Applicant = Applicant
        self.Duration = Duration
        self.Events = self.Applicant.Events

    @abstractmethod
    def InitialiseEffect(self):
        pass

    @abstractmethod
    def DestroyEffect(self):
        pass

    @abstractmethod
    def Listener(self):
        pass