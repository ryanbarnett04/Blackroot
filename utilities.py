import random
from enum import Enum
from typing import TYPE_CHECKING
from dataclasses import dataclass
from Events.damage_instance_single import DamageInstanceSingle
from Events.heal_instance_single import HealInstanceSingle

if TYPE_CHECKING:
    from character import Character
    from ability import Ability

class StatusType(Enum):
    Default = 1
    NoDamage = 2
    Evaded = 3
    DamageDealt = 4

@dataclass
class DamageStatus:
    Type: StatusType = StatusType.Default
    Damage: int = -1
    WasCrit: bool | None = None

# TODO: Redesign defence system to not use flat defence - to overpowered (do not do pure percentile defence either)
def CalculateDamage(ActiveAbility: "Ability", Target: "Character",
                       AbilityDamage: float, VarianceRange: list[float]) -> DamageStatus:

    if "DAMAGE_IMMUNE" in Target.EffectTags:
        return DamageStatus(Type = StatusType.NoDamage)

    if "GUARANTEED_EVADE" in Target.EffectTags or random.randint(1,100) <= Target.GetCurrentEvasion():
        print("Evaded!")
        return DamageStatus(Type = StatusType.Evaded)

    AttackDamage = (ActiveAbility.User.GetCurrentOffence() * AbilityDamage) - Target.GetCurrentDefence()
    IsCrit = False

    if AttackDamage < 0:
        AttackDamage = 0

    if "CRIT_IMMUNE" not in Target.EffectTags:
        if "GUARANTEED_CRIT" in ActiveAbility.User.EffectTags or random.randint(1,100) <= ActiveAbility.User.GetCurrentCriticalChance():
            AttackDamage = AttackDamage * (ActiveAbility.User.GetCurrentCriticalDamage() / 100)
            IsCrit = True

    Variance = random.uniform(VarianceRange[0], VarianceRange[1])
    AttackDamage = AttackDamage * (1 + Variance)
    AttackDamage = int(AttackDamage)

    return DamageStatus(Type = StatusType.DamageDealt, Damage = AttackDamage, WasCrit = IsCrit)

def SingleTargetDamage(ActiveAbility: "Ability", Target: "Character",
                       AbilityDamage: float, VarianceRange: list[float]):

    DamageInfo = CalculateDamage(ActiveAbility, Target, AbilityDamage, VarianceRange)

    if DamageInfo.Type == StatusType.NoDamage:
        return

    if DamageInfo.Type == StatusType.Evaded:
        # TODO: Distribute Evasion event here but evasion event not implemented yet
        return

    Target.ReceiveDamage(ActiveAbility, DamageInfo.Damage)
    ActiveAbility.User.Events.DistributeEvent(DamageInstanceSingle(ActiveAbility.User, Target, DamageInfo.Damage, bool(DamageInfo.WasCrit)))

    if "CANNOT_RECOVER_HEALTH" not in ActiveAbility.User.EffectTags:
        Recovery = int(DamageInfo.Damage * (ActiveAbility.User.GetCurrentHealthSteal() / 100))
        ActiveAbility.User.ModifyCurrentHealth(Recovery)
        ActiveAbility.User.Events.DistributeEvent(HealInstanceSingle(ActiveAbility.User, ActiveAbility.User, Recovery))

def MultiTargetDamage(ActiveAbility: "Ability", Targets: list["Character"],
                      AbilityDamage: float, VarianceRange: list[float]):
    # TODO: Implement MultiTargetDamage
    pass

def GrantBuffSingle():
    # TODO: Implement GrantBuffSingle
    pass

def GrantBuffMultiple():
    # TODO: Implement GrantBuffMultiple
    pass

def InflictDebuffSingle():
    # TODO: Implement InflictDebuffSingle
    pass

def InflictDebuffMultiple():
    # TODO: Implement InflictDebuffMultiple
    pass