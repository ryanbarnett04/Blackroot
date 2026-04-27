from ability import *
from enum import Enum
from event_pipeline import EventPipeline

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ability import Ability
    from status_effect import StatusEffect

class CharacterRole(Enum):
    Attacker = 1
    Tank = 2
    Support = 3

class CharacterSide(Enum):
    AllySide = 1
    EnemySide = 2

class Character:

    Name: str
    Leader: bool
    Role: CharacterRole
    Tags: list[str]
    HiddenTags: list[str]
    Side: CharacterSide

    # Health Stats & Attributes
    BaseMaxHealth: int
    CurrentMaxHealth: int
    PercentileMaxHealthModifier: float
    FlatMaxHealthModifier: int
    CurrentHealth: int

    CanRecoverHealth: bool = True
    CanGainMaxHealth: bool = True
    CanLoseMaxHealth: bool = True

    # Shield Stats & Attributes
    BaseMaxShield: int
    CurrentMaxShield: int
    PercentileMaxShieldModifier: float
    FlatMaxShieldModifier: int
    CurrentShield: int

    CanRecoverShield: bool = True
    CanGainMaxShield: bool = True
    CanLoseMaxShield: bool = True

    # Offence Stats & Attributes
    BaseOffence: int
    CurrentOffence: int
    PercentileOffenceModifier: float
    FlatOffenceModifier: int

    CanGainOffence: bool = True
    CanLoseOffence: bool = True

    # Defence Stats & Attributes
    BaseDefence: int
    CurrentDefence: int
    PercentileDefenceModifier: float
    FlatDefenceModifier: int

    CanGainDefence: bool = True
    CanLoseDefence: bool = True

    # Critical Chance Stats & Attributes
    BaseCriticalChance: int
    CurrentCriticalChance: int
    PercentileCriticalChanceModifier: float

    CanGainCriticalChance: bool = True
    CanLoseCriticalChance: bool = True

    # Critical Damage Stats & Attributes
    BaseCriticalDamage: int
    CurrentCriticalDamage: int
    PercentileCriticalDamageModifier: float

    CanGainCriticalDamage: bool = True
    CanLoseCriticalDamage: bool = True

    # Evasion Stats & Attributes
    BaseEvasion: int
    CurrentEvasion: int
    PercentileEvasionModifier: float

    CanGainEvasion: bool = True
    CanLoseEvasion: bool = True

    # Health Steal Stats & Attributes
    BaseHealthSteal: int
    CurrentHealthSteal: int
    PercentileHealthStealModifier: float

    CanGainHealthSteal: bool = True
    CanLoseHealthSteal: bool = True

    # Speed Stats & Attributes
    BaseSpeed: int
    CurrentSpeed: int
    PercentileSpeedModifier: float
    FlatSpeedModifier: int
    TurnMeter: float                    # 0.0 -> 1.0

    CanGainSpeed: bool = True
    CanLoseSpeed: bool = True

    # Other Attributes
    IsAlive: bool = True
    CanReceiveDamage: bool = True
    CanBeCriticallyHit: bool = True
    CanGainBonusTM: bool = True
    CanLoseBonusTM: bool = True
    CanGainBuffs: bool = True
    CanGainDebuffs: bool = True
    GuaranteedEvade: bool = False
    GuaranteedCrit: bool = False
    Stunned: bool = False
    CanAssist: bool = True

    Events: EventPipeline
    ActiveAbilities: list["Ability"]
    PassiveAbilities: list["Ability"]
    StatusEffects: list["StatusEffect"]
    EffectTags: list[str]

    def __init__(self, Name, Leader, Role, Tags, HiddenTags, Side,
                 BaseMaxHealth, BaseMaxShield, BaseOffence, BaseDefence, BaseCriticalChance,
                 BaseCriticalDamage, BaseEvasion, BaseHealthSteal, BaseSpeed):

        self.Name = Name
        self.Leader = Leader
        self.Role = Role
        self.Tags = Tags
        self.HiddenTags = HiddenTags
        self.Side = Side
        self.BaseMaxHealth = BaseMaxHealth
        self.CurrentMaxHealth = BaseMaxHealth
        self.CurrentHealth = BaseMaxHealth
        self.PercentileMaxHealthModifier = 0.0
        self.FlatMaxHealthModifier = 0
        self.BaseMaxShield = BaseMaxShield
        self.CurrentMaxShield = BaseMaxShield
        self.CurrentShield = BaseMaxShield
        self.PercentileMaxShieldModifier = 0.0
        self.FlatMaxShieldModifier = 0
        self.BaseOffence = BaseOffence
        self.CurrentOffence = BaseOffence
        self.PercentileOffenceModifier = 0.0
        self.FlatOffenceModifier = 0
        self.BaseDefence = BaseDefence
        self.CurrentDefence = BaseDefence
        self.PercentileDefenceModifier = 0.0
        self.FlatDefenceModifier = 0
        self.BaseCriticalChance = BaseCriticalChance
        self.CurrentCriticalChance = BaseCriticalChance
        self.PercentileCriticalChanceModifier = 0.0
        self.BaseCriticalDamage = BaseCriticalDamage
        self.CurrentCriticalDamage = BaseCriticalDamage
        self.PercentileCriticalDamageModifier = 0.0
        self.BaseEvasion = BaseEvasion
        self.CurrentEvasion = BaseEvasion
        self.PercentileEvasionModifier = 0.0
        self.BaseHealthSteal = BaseHealthSteal
        self.CurrentHealthSteal = BaseHealthSteal
        self.PercentileHealthStealModifier = 0.0
        self.BaseSpeed = BaseSpeed
        self.CurrentSpeed = BaseSpeed
        self.PercentileSpeedModifier = 0.0
        self.FlatSpeedModifier = 0
        self.TurnMeter = 0.0
        self.StatusEffects = []
        self.EffectTags = []

    # Health
    def SetCurrentMaxHealth(self):
        self.CurrentMaxHealth = int(self.BaseMaxHealth * (1 + self.PercentileMaxHealthModifier) + self.FlatMaxHealthModifier)

        if self.CurrentMaxHealth < 1:
            self.CurrentMaxHealth = 1

        if self.CurrentHealth > self.CurrentMaxHealth:
            self.CurrentHealth = self.CurrentMaxHealth

    def GetCurrentMaxHealth(self):
        return self.CurrentMaxHealth

    def SetPercentileMaxHealthModifier(self, modifier: float):
        self.PercentileMaxHealthModifier = self.PercentileMaxHealthModifier + modifier
        self.SetCurrentMaxHealth()

    def GetPercentileMaxHealthModifier(self):
        return self.PercentileMaxHealthModifier

    def SetFlatMaxHealthModifier(self, modifier: int):
        self.FlatMaxHealthModifier = self.FlatMaxHealthModifier + modifier
        self.SetCurrentMaxHealth()

    def GetFlatMaxHealthModifier(self):
        return self.FlatMaxHealthModifier

    def ModifyCurrentHealth(self, modifier: int):
        self.CurrentHealth = self.CurrentHealth + modifier

        if self.CurrentHealth <= 0:
            print("They Died")

        if self.CurrentHealth > self.CurrentMaxHealth:
            self.CurrentHealth = self.CurrentMaxHealth

    def GetCurrentHealth(self):
        return self.CurrentHealth

    # Shield
    def SetCurrentMaxShield(self):
        self.CurrentMaxShield = int(self.BaseMaxShield * (1 + self.PercentileMaxShieldModifier) + self.FlatMaxShieldModifier)

        if self.CurrentMaxShield < 1:
            self.CurrentMaxShield = 1

        if self.CurrentShield > self.CurrentMaxShield:
            self.CurrentShield = self.CurrentMaxShield

    def GetCurrentMaxShield(self):
        return self.CurrentMaxShield

    def SetPercentileMaxShieldModifier(self, modifier: float):
        self.PercentileMaxShieldModifier = self.PercentileMaxShieldModifier + modifier
        self.SetCurrentMaxShield()

    def GetPercentileMaxShieldModifier(self):
        return self.PercentileMaxShieldModifier

    def SetFlatMaxShieldModifier(self, modifier: int):
        self.FlatMaxShieldModifier = self.FlatMaxShieldModifier + modifier
        self.SetCurrentMaxShield()

    def GetFlatMaxShieldModifier(self):
        return self.FlatMaxShieldModifier

    def ModifyCurrentShield(self, modifier: int):
        self.CurrentShield = self.CurrentShield + modifier

        if self.CurrentShield <= 0:
            self.CurrentShield = 0

        if self.CurrentShield > self.CurrentMaxShield:
            self.CurrentShield = self.CurrentMaxShield

    def GetCurrentShield(self):
        return self.CurrentShield

    # Offence
    def ModifyCurrentOffence(self):
        self.CurrentOffence = int(self.BaseOffence * (1 + self.PercentileOffenceModifier) + self.FlatOffenceModifier)

    def GetCurrentOffence(self):
        return self.CurrentOffence

    def SetPercentileOffenceModifier(self, modifier: float):
        self.PercentileOffenceModifier = self.PercentileOffenceModifier + modifier
        self.ModifyCurrentOffence()

    def GetPercentileOffenceModifier(self):
        return self.PercentileOffenceModifier

    def SetFlatOffenceModifier(self, modifier: int):
        self.FlatOffenceModifier = self.FlatOffenceModifier + modifier
        self.ModifyCurrentOffence()

    def GetFlatOffenceModifier(self):
        return self.FlatOffenceModifier

    # Defence
    def ModifyCurrentDefence(self):
        self.CurrentDefence = int(self.BaseDefence * (1 + self.PercentileDefenceModifier) + self.FlatDefenceModifier)

    def GetCurrentDefence(self):
        return self.CurrentDefence

    def SetPercentileDefenceModifier(self, modifier: float):
        self.PercentileDefenceModifier = self.PercentileDefenceModifier + modifier
        self.ModifyCurrentDefence()

    def GetPercentileDefenceModifier(self):
        return self.PercentileDefenceModifier

    def SetFlatDefenceModifier(self, modifier: int):
        self.FlatDefenceModifier = self.FlatDefenceModifier + modifier
        self.ModifyCurrentDefence()

    def GetFlatDefenceModifier(self):
        return self.FlatDefenceModifier

    # Critical Chance
    def ModifyCurrentCriticalChance(self):
        self.CurrentCriticalChance = int(self.BaseCriticalChance * (1 + self.PercentileCriticalChanceModifier))

    def GetCurrentCriticalChance(self):
        return self.CurrentCriticalChance

    def SetPercentileCriticalChanceModifier(self, modifier: float):
        self.PercentileCriticalChanceModifier = self.PercentileCriticalChanceModifier + modifier
        self.ModifyCurrentCriticalChance()

    def GetPercentileCriticalChanceModifier(self):
        return self.PercentileCriticalChanceModifier

    # Critical Damage
    def ModifyCurrentCriticalDamage(self):
        self.CurrentCriticalDamage = int(self.BaseCriticalDamage * (1 + self.PercentileCriticalDamageModifier))

    def GetCurrentCriticalDamage(self):
        return self.CurrentCriticalDamage

    def SetPercentileCriticalDamageModifier(self, modifier: float):
        self.PercentileCriticalDamageModifier = self.PercentileCriticalDamageModifier + modifier
        self.ModifyCurrentCriticalDamage()

    def GetPercentileCriticalDamageModifier(self):
        return self.PercentileCriticalDamageModifier

    # Evasion
    def ModifyCurrentEvasion(self):
        self.CurrentEvasion = int(self.BaseEvasion * (1 + self.PercentileEvasionModifier))

    def GetCurrentEvasion(self):
        return self.CurrentEvasion

    def SetPercentileEvasionModifier(self, modifier: float):
        self.PercentileEvasionModifier = self.PercentileEvasionModifier + modifier
        self.ModifyCurrentEvasion()

    def GetPercentileEvasionModifier(self):
        return self.PercentileEvasionModifier

    # Health Steal
    def ModifyCurrentHealthSteal(self):
        self.CurrentHealthSteal = int(self.BaseHealthSteal * (1 + self.PercentileHealthStealModifier))

    def GetCurrentHealthSteal(self):
        return self.CurrentHealthSteal

    def SetPercentileHealthStealModifier(self, modifier: float):
        self.PercentileHealthStealModifier = self.PercentileHealthStealModifier + modifier
        self.ModifyCurrentHealthSteal()

    def GetPercentileHealthStealModifier(self):
        return self.PercentileHealthStealModifier

    # Speed
    def ModifyCurrentSpeed(self):
        self.CurrentSpeed = int(self.BaseSpeed * (1 + self.PercentileSpeedModifier) + self.FlatSpeedModifier)

    def GetCurrentSpeed(self):
        return self.CurrentSpeed

    def SetPercentileSpeedModifier(self, modifier: float):
        self.PercentileSpeedModifier = self.PercentileSpeedModifier + modifier
        self.ModifyCurrentSpeed()

    def GetPercentileSpeedModifier(self):
        return self.PercentileSpeedModifier

    def SetFlatSpeedModifier(self, modifier: int):
        self.FlatSpeedModifier = self.FlatSpeedModifier + modifier
        self.ModifyCurrentSpeed()

    def GetFlatSpeedModifier(self):
        return self.FlatSpeedModifier

    def ModifyTurnMeter(self, modifier):
        self.TurnMeter = self.TurnMeter + modifier

        if self.TurnMeter > 1.0:
            self.TurnMeter = 1.0
        elif self.TurnMeter < 0.0:
            self.TurnMeter = 0.0

    def SetTurnMeter(self, TM: float):
        self.TurnMeter = TM

    def GetTurnMeter(self):
        return self.TurnMeter