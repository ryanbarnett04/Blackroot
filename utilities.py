import random
from typing import TYPE_CHECKING

from Events.damage_instance_single import DamageInstanceSingle

if TYPE_CHECKING:
    from character import Character
    from ability import Ability

def SingleTargetDamage(ActiveAbility: "Ability", Target: "Character",
                       AbilityDamage: float, VarianceRange: list[float]):

    if not Target.CanReceiveDamage:
        return

    if Target.GuaranteedEvade or random.randint(1, 100) <= Target.GetCurrentEvasion():
        print("Evaded!")
        return

    AttackDamage = (ActiveAbility.User.GetCurrentOffence() * AbilityDamage) - Target.GetCurrentDefence()
    IsCrit = False

    if AttackDamage < 0:
        AttackDamage = 0

    if Target.CanBeCriticallyHit:
        if ActiveAbility.User.GuaranteedCrit or random.randint(1, 100) <= ActiveAbility.User.GetCurrentCriticalChance():
            AttackDamage = AttackDamage * (ActiveAbility.User.GetCurrentCriticalDamage() / 100)
            IsCrit = True

    Variance = random.uniform(VarianceRange[0], VarianceRange[1])
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

    if ActiveAbility.User.CanRecoverHealth:
        ActiveAbility.User.ModifyCurrentHealth(int(AttackDamage * (ActiveAbility.User.GetCurrentHealthSteal() / 100)))

    ActiveAbility.User.Events.DistributeEvent(DamageInstanceSingle(ActiveAbility.User, Target, AttackDamage, IsCrit))

    print(f"{ActiveAbility.Name} - Damage: {AttackDamage}")