from status_effect import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from event import Event

class SpeedUp(StatusEffect):

    def __init__(self, Applicant: "Character", Duration: int, Dispellable: bool, Copyable: bool):
        super().__init__(Applicant, Duration, Dispellable, Copyable)
        self.Name = "Speed Up"
        self.Type = EffectType.Buff
        self.Description = '''
        +25% Speed 
        '''

        self.InitialiseEffect()

    def InitialiseEffect(self):

        if not "SPEED_UP" in self.Applicant.EffectTags:
            self.Applicant.SetPercentileSpeedModifier(0.25)

        self.Applicant.EffectTags.append("SPEED_UP")

        self.Applicant.Events.RegisteredEffects.append(self)

    def DestroyEffect(self):

        self.Applicant.EffectTags.remove("SPEED_UP")

        if not "SPEED_UP" in self.Applicant.EffectTags:
            self.Applicant.SetPercentileSpeedModifier(-0.25)

        self.Applicant.Events.RegisteredEffects.remove(self)
        self.Applicant.StatusEffects.remove(self)

    def Listener(self, event: "Event"):
        pass