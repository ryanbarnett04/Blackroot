from Events.basic_ability_used import BasicAbilityUsed
from character import Character, CharacterRole, CharacterSide
from ability import Ability, AbilityType
from StatusEffects.offence_up import OffenceUp
import random

from event import Event, EventType
from event_pipeline import EventPipeline
from Events.damage_instance_single import DamageInstanceSingle
from Events.basic_ability_used import BasicAbilityUsed
from Events.special_ability_used import SpecialAbilityUsed
class OrcChieftain(Character):

    def __init__(self, Side: CharacterSide, Events: EventPipeline):

        super().__init__(Name = "Orc Chieftain", Leader = True, Role = CharacterRole.Support,
                       Tags = ["Orc"], HiddenTags = ["SELFTAG_ORCCHIEFTAIN"], Side = Side, BaseMaxHealth = 66880, BaseMaxShield = 48153,
                       BaseOffence = 5889, BaseDefence = 5127, BaseCriticalChance = 54, BaseCriticalDamage = 150,
                       BaseEvasion = 10, BaseHealthSteal = 15, BaseSpeed = 160)

        self.Events = Events

        self.ActiveAbilities = [
            OrcChieftain.BannerStrike(self),
            OrcChieftain.Warcry(self)
        ]

        self.PassiveAbilities = [
            OrcChieftain.WarChief(self)
        ]

        self.Events.RegisteredAbilities.append(self.ActiveAbilities[0])
        self.Events.RegisteredAbilities.append(self.ActiveAbilities[1])
        self.Events.RegisteredAbilities.append(self.PassiveAbilities[0])

    # BASIC ABILITY - BANNER STRIKE:
    # Deal 250% Damage to target enemy
    class BannerStrike(Ability):

        def __init__(self, User: Character):

            super().__init__(User = User, Name = "Banner Strike", Type = AbilityType.Basic,
                             Cooldown = None, TurnsToNextUse = None)

        def Activate(self, Allies: list[Character], Enemies: list[Character], TargetAllyIndex: int, TargetEnemyIndex: int):

            Target = Enemies[TargetEnemyIndex]

            if not Target.CanReceiveDamage:
                return

            if Target.GuaranteedEvade or random.randint(1, 100) <= Target.GetCurrentEvasion():
                print("Evaded!")
                return

            AttackDamage = (self.User.GetCurrentOffence() * 2.5) - Target.GetCurrentDefence()
            IsCrit = False

            if AttackDamage < 0:
                AttackDamage = 0

            if Target.CanBeCriticallyHit:
                if self.User.GuaranteedCrit or random.randint(1, 100) <= self.User.GetCurrentCriticalChance():
                    AttackDamage = AttackDamage * (self.User.GetCurrentCriticalDamage() / 100)
                    IsCrit = True

            Variance = random.uniform(-0.10, 0.10)
            AttackDamage = AttackDamage * (1 + Variance)

            AttackDamage = int(AttackDamage)

            if Target.GetCurrentShield() > 0:

                if Target.GetCurrentShield() < AttackDamage:
                    ShieldDamage = Target.GetCurrentShield()
                    HealthDamage = AttackDamage - ShieldDamage
                    Target.ModifyCurrentShield(-ShieldDamage)
                    Target.ModifyCurrentHealth(-HealthDamage)
                else:
                    Target.ModifyCurrentShield(-AttackDamage)
            else:
                Target.ModifyCurrentHealth(-AttackDamage)

            print(self.Name)
            print("Damage:", AttackDamage)

            if self.User.CanRecoverHealth:
                self.User.ModifyCurrentHealth(int(AttackDamage * (self.User.GetCurrentHealthSteal() / 100)))

            self.User.Events.DistributeEvent(BasicAbilityUsed(self.User))
            self.User.Events.DistributeEvent(DamageInstanceSingle(self.User, Target, AttackDamage, IsCrit))

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
                    Ally.StatusEffects.append(OffenceUp(self.User, 2))

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