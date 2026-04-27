from status_effect import *

class OffenceUp(StatusEffect):

    def __init__(self, Applicant: "Character", Duration: int):
        super().__init__(Applicant, Duration)
        self.Name = "Offence Up"
        self.Type = EffectType.Buff
        self.Description = '''
        +50% Offence 
        '''

        self.InitialiseEffect()

    def InitialiseEffect(self):

        if not "OFFENCE_UP" in self.Applicant.EffectTags:
            self.Applicant.SetPercentileOffenceModifier(0.5)

        self.Applicant.EffectTags.append("OFFENCE_UP")

    def DestroyEffect(self):

        self.Applicant.EffectTags.remove("OFFENCE_UP")

        if not "OFFENCE_UP" in self.Applicant.EffectTags:
            self.Applicant.SetPercentileOffenceModifier(-0.5)

    def Listener(self):
        pass