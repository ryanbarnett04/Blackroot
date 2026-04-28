from Events.damage_instance_mulitple import DamageInstanceMultiple
from Events.new_turn import NewTurn
from character import Character, CharacterRole, CharacterSide
from ability import Ability, AbilityType
from StatusEffects.offence_up import OffenceUp
from event import Event
from event_pipeline import EventPipeline
from Events.damage_instance_single import DamageInstanceSingle
from Events.basic_ability_used import BasicAbilityUsed
from Events.special_ability_used import SpecialAbilityUsed
from utilities import SingleTargetDamage

class OrcChieftain(Character):

    def __init__(self, Side: CharacterSide, Events: EventPipeline):

        super().__init__(Name = "Orc Chieftain", Leader = True, Role = CharacterRole.Support,
                       Tags = ["Orc"], HiddenTags = ["SELFTAG_ORCCHIEFTAIN"], Side = Side, BaseMaxHealth = 66880, BaseMaxShield = 48153,
                       BaseOffence = 5889, BaseDefence = 4972, BaseCriticalChance = 54, BaseCriticalDamage = 150,
                       BaseEvasion = 2, BaseHealthSteal = 20, BaseSpeed = 200)

        self.Events = Events

        self.ActiveAbilities = [
            OrcChieftain.BannerStrike(self),
            OrcChieftain.Warcry(self)
        ]

        self.PassiveAbilities = [
            OrcChieftain.WarChief(self),
            OrcChieftain.Commander(self)
        ]

        self.Events.RegisteredAbilities.append(self.ActiveAbilities[0])
        self.Events.RegisteredAbilities.append(self.ActiveAbilities[1])
        self.Events.RegisteredAbilities.append(self.PassiveAbilities[0])
        self.Events.RegisteredAbilities.append(self.PassiveAbilities[1])

    # BASIC ABILITY - BANNER STRIKE:
    # Deal 250% Damage to target enemy and grant a random ally Speed Up for 1 turn
    class BannerStrike(Ability):

        def __init__(self, User: Character):

            super().__init__(User = User, Name = "Banner Strike", Type = AbilityType.Basic,
                             Cooldown = None, TurnsToNextUse = None)

        def Activate(self, Allies: list[Character], Enemies: list[Character], TargetAllyIndex: int, TargetEnemyIndex: int):

            self.User.Events.DistributeEvent(BasicAbilityUsed(self.User))
            Target = Enemies[TargetEnemyIndex]
            SingleTargetDamage(self, Target, 2.5, [-0.10, 0.10])
            return

        def Listener(self, event: Event):

            print("Ability: ", self.Name, " from ", self.User.Name, " from ", self.User.Side, " is reacting to event")

    # SPECIAL ABILITY - WARCRY
    # All allies gain Offence Up for 2 turns and 20% Turn Meter
    class Warcry(Ability):

        def __init__(self, User: Character):
            super().__init__(User = User, Name = "Warcry", Type = AbilityType.Special,
                             Cooldown = 3, TurnsToNextUse = 0)

        def Activate(self, Allies: list[Character], Enemies: list[Character], TargetAllyIndex: int, TargetEnemyIndex: int):

            for Ally in Allies:

                if Ally.CanGainBuffs:
                    Ally.StatusEffects.append(OffenceUp(Ally, 2))

                if Ally.CanGainBonusTM:
                    Ally.ModifyTurnMeter(0.2)

            self.TurnsToNextUse = self.Cooldown

            self.User.Events.DistributeEvent(SpecialAbilityUsed(self.User))

            return

        def Listener(self, event: Event):
            print("Ability: ", self.Name, " from ", self.User.Name, " from ", self.User.Side, " is reacting to event")

    # LEADER ABILITY - WAR CHIEF
    # Allies gain +30% Max Health and +20% Offence. Orc allies gain 5% Turn Meter whenever they score a critical hit
    class WarChief(Ability):

        def __init__(self, User: Character):
            super().__init__(User = User, Name = "War Chief", Type = AbilityType.Leader,
                             Cooldown = None, TurnsToNextUse = None)

        def Activate(self, Allies: list[Character], Enemies: list[Character], TargetEnemyIndex: int, TargetAllyIndex: int):

            for Ally in Allies:

                if Ally.CanGainMaxHealth:
                    Ally.SetPercentileMaxHealthModifier(0.3)

                if Ally.CanGainOffence:
                    Ally.SetPercentileOffenceModifier(0.2)

        def Listener(self, event: Event):

            print("Ability: ", self.Name, " from ", self.User.Name, " from ", self.User.Side, " is reacting to event")

            if isinstance(event, DamageInstanceSingle):
                if event.GeneratedBy.Side == self.User.Side:
                    if "Orc" in event.GeneratedBy.Tags:
                        if event.WasCrit:
                            event.GeneratedBy.ModifyTurnMeter(0.05)

            if isinstance(event, DamageInstanceMultiple):
                if event.GeneratedBy.Side == self.User.Side:
                    if "Orc" in event.GeneratedBy.Tags:
                        crits = event.WasCrit.count(True)
                        if crits > 0:
                            event.GeneratedBy.ModifyTurnMeter(0.05 * crits)

    # UNIQUE ABILITY - Commander
    # Orc Chieftain gains 20% Max Shield. Whenever an Orc ally is Critically Hit, they recover 10% Health and Orc Chieftain gains 10% Turn Meter (limit once per turn)
    class Commander(Ability):

        def __init__(self, User: Character):
            super().__init__(User = User, Name = "Commander", Type = AbilityType.Unique,
                             Cooldown = None, TurnsToNextUse = None)

            self.CanGainTM = True

        def Activate(self, Allies: list["Character"], Enemies: list["Character"], TargetEnemyIndex: int, TargetAllyIndex: int):

            if self.User.CanGainMaxShield:
                self.User.SetPercentileMaxShieldModifier(0.2)

        def Listener(self, event: "Event"):

            if isinstance(event, DamageInstanceSingle):
                if event.GeneratedBy.Side == self.User.Side:
                    return
                if "Orc" not in event.Receiver.Tags:
                    return
                if not event.WasCrit:
                    return
                if event.Receiver.CanRecoverHealth:
                    event.Receiver.ModifyCurrentHealth(event.Receiver.GetCurrentMaxHealth() * (10 / 100))
                if self.User.CanGainBonusTM and self.CanGainTM:
                    self.User.ModifyTurnMeter(0.10)
                    self.CanGainTM = False

            if isinstance(event, DamageInstanceMultiple):
                if event.GeneratedBy.Side == self.User.Side:
                    return
                for i, C in enumerate(event.Receivers):
                    if "Orc" not in C.Tags:
                        continue
                    if not event.WasCrit[i]:
                        continue
                    if C.CanRecoverHealth:
                        C.ModifyCurrentHealth(C.GetCurrentMaxHealth() * (10 / 100))
                    if self.User.CanGainBonusTM and self.CanGainTM:
                        self.User.ModifyTurnMeter(0.10)
                        self.CanGainTM = False

            if isinstance(event, NewTurn):
                self.CanGainTM = True