import random
from character import Character, CharacterRole, CharacterSide
from ability import Ability, AbilityType
from event import Event
from event_pipeline import EventPipeline
from Events.damage_instance_single import DamageInstanceSingle
from Events.basic_ability_used import BasicAbilityUsed
from utilities import SingleTargetDamage


class OrcWarrior(Character):

    def __init__(self, Side: CharacterSide, Events: EventPipeline):

        super().__init__(Name = "Orc Warrior", Leader = False, Role = CharacterRole.Attacker,
                       Tags = ["Orc"], HiddenTags = ["SELFTAG_ORCWARRIOR"], Side = Side, BaseMaxHealth = 59746, BaseMaxShield = 45160,
                       BaseOffence = 7143, BaseDefence = 3677, BaseCriticalChance = 101, BaseCriticalDamage = 172,
                       BaseEvasion = 2, BaseHealthSteal = 15, BaseSpeed = 163)

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

            self.User.Events.DistributeEvent(BasicAbilityUsed(self.User))
            Target = Enemies[TargetEnemyIndex]
            SingleTargetDamage(self, Target, 2.5, [-0.10, 0.10])

            return

        def Listener(self, event: Event):

            print("Ability: ", self.Name, " from ", self.User.Name, " from ", self.User.Side, " is reacting to event")