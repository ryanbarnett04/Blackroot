from status_effect import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from event import Event

class DefenceDown(StatusEffect):

    def __init__(self, Applicant: "Character", Duration: int, Dispellable: bool, Copyable: bool):
        super().__init__(Applicant, Duration, Dispellable, Copyable)
        self.Name = "Defence Down"
        self.Type = EffectType.Debuff
        self.Description = '''
        -50% Defence
        '''

        self.InitialiseEffect()

    def InitialiseEffect(self):

        if not "DEFENCE_DOWN" in self.Applicant.EffectTags:
            self.Applicant.SetPercentileDefenceModifier(-0.5)

        self.Applicant.EffectTags.append("DEFENCE_DOWN")

    def DestroyEffect(self):

        self.Applicant.EffectTags.remove("DEFENCE_DOWN")

        if not "DEFENCE_DOWN" in self.Applicant.EffectTags:
            self.Applicant.SetPercentileDefenceModifier(0.5)

    def Listener(self, event: "Event"):
        pass