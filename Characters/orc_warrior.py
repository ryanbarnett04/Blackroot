from event import Event
from Events.basic_ability_used import BasicAbilityUsed
from Events.damage_instance_single import DamageInstanceSingle
from character import *
from ability import *
import random

class OrcWarrior(Character):

    def __init__(self, Side: CharacterSide, Events: EventPipeline):

        super().__init__(Name = "Orc Warrior", Leader = False, Role = CharacterRole.Attacker,
                       Tags = ["Orc"], HiddenTags = ["SELFTAG_ORCWARRIOR"], Side = Side, BaseMaxHealth = 108378, BaseMaxShield = 60274,
                       BaseOffence = 6174, BaseDefence = 3185, BaseCriticalChance = 67, BaseCriticalDamage = 150,
                       BaseEvasion = 0, BaseHealthSteal = 10, BaseSpeed = 156)

        self.Events = Events

        self.ActiveAbilities = [
            OrcWarrior.Cleave(self)
        ]

        self.PassiveAbilities = [
            #
        ]

        self.Events.RegisteredAbilities.append(self.ActiveAbilities[0])

    # BASIC ABILITY - BANNER STRIKE:
    # Deal 300% Damage to target enemy
    class Cleave(Ability):

        def __init__(self, User: Character):

            super().__init__(User = User, Name = "Cleave", Type = AbilityType.Basic,
                             Cooldown = None, TurnsToNextUse = None)

        def Activate(self, Allies: list[Character], Enemies: list[Character], TargetAllyIndex: int,
                     TargetEnemyIndex: int):

            Target = Enemies[TargetEnemyIndex]

            if not Target.CanReceiveDamage:
                return

            if Target.GuaranteedEvade or random.randint(1, 100) <= Target.GetCurrentEvasion():
                print("Evaded!")
                return

            AttackDamage = (self.User.GetCurrentOffence() * 3.0) - Target.GetCurrentDefence()
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