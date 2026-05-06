from character import Character, CharacterRole, CharacterSide
from ability import Ability, AbilityType
from event import Event
from event_pipeline import EventPipeline
from Events.basic_ability_used import BasicAbilityUsed
from Events.special_ability_used import SpecialAbilityUsed

class CharacterName(Character):

    def __init__(self, Side: CharacterSide, Events: EventPipeline):

        super().__init__(Name = "Name", Leader = True, Role = CharacterRole.Attacker,
                       Tags = ["X Faction", "Y Faction"], HiddenTags = ["SELFTAG_NAME"], Side = Side, BaseMaxHealth = 66880, BaseMaxShield = 48153,
                       BaseOffence = 5889, BaseDefence = 4972, BaseCriticalChance = 54, BaseCriticalDamage = 150,
                       BaseEvasion = 2, BaseHealthSteal = 20, BaseSpeed = 150)

        self.Events = Events

        self.ActiveAbilities = [
            # Instantiate Active Abilities Here - Basic, Special, Granted
        ]

        self.PassiveAbilities = [
            # Instantiate Passive Abilities Here - Leader, Unique, Granted
        ]

        # Register all abilities into the event pipeline - For Example:
        # self.Events.RegisteredAbilities.append(self.ActiveAbilities[0])
        # self.Events.RegisteredAbilities.append(self.PassiveAbilities[0])

    # BASIC ABILITY - NAME:
    # Ability Description
    class BasicName(Ability):

        def __init__(self, User: Character):

            super().__init__(User = User, Name = "Name", Type = AbilityType.Basic,
                             Cooldown = None, TurnsToNextUse = None)

        def Activate(self, Allies: list[Character], Enemies: list[Character], TargetAllyIndex: int, TargetEnemyIndex: int):

            self.User.Events.DistributeEvent(BasicAbilityUsed(self.User))
            # Implementation

        def Listener(self, event: Event):

            # Implementation
            pass

    # SPECIAL ABILITY - NAME
    # Ability Description
    class SpecialName(Ability):

        def __init__(self, User: Character):
            super().__init__(User = User, Name = "Name", Type = AbilityType.Special,
                             Cooldown = 3, TurnsToNextUse = 0)

        def Activate(self, Allies: list[Character], Enemies: list[Character], TargetAllyIndex: int, TargetEnemyIndex: int):

            self.User.Events.DistributeEvent(SpecialAbilityUsed(self.User))

            # Implementation

            self.TurnsToNextUse = self.Cooldown

            return

        def Listener(self, event: Event):

            # Implementation
            pass

    # LEADER ABILITY - NAME
    # Ability Description
    class LeaderName(Ability):

        def __init__(self, User: Character):
            super().__init__(User = User, Name = "Name", Type = AbilityType.Leader,
                             Cooldown = None, TurnsToNextUse = None)

        def Activate(self, Allies: list[Character], Enemies: list[Character], TargetEnemyIndex: int, TargetAllyIndex: int):

            # Implementation
            pass

        def Listener(self, event: Event):

            # Implementation
            pass

    # UNIQUE ABILITY - NAME
    # Ability Description
    class UniqueName(Ability):

        def __init__(self, User: Character):
            super().__init__(User = User, Name = "Name", Type = AbilityType.Unique,
                             Cooldown = None, TurnsToNextUse = None)

        def Activate(self, Allies: list["Character"], Enemies: list["Character"], TargetEnemyIndex: int, TargetAllyIndex: int):

            # Implementation
            pass

        def Listener(self, event: "Event"):

            # Implementation
            pass