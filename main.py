import sys
import pygame
from character import Character, CharacterSide
from Characters.orc_chieftain import OrcChieftain
from Characters.orc_warrior import OrcWarrior
from Characters.orc_brute import OrcBrute
from event_pipeline import EventPipeline
from turn_manager import TurnManager

pygame.init()
screen = pygame.display.set_mode((100,100))
pygame.display.set_caption("SWGOH Clone")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 20)
EventPipeline = EventPipeline()

AllyLeader = OrcChieftain(CharacterSide.AllySide, EventPipeline)
AllyTwo = OrcWarrior(CharacterSide.AllySide, EventPipeline)
AllyThree = OrcBrute(CharacterSide.AllySide, EventPipeline)

EnemyLeader = OrcChieftain(CharacterSide.EnemySide, EventPipeline)
EnemyTwo = OrcWarrior(CharacterSide.EnemySide, EventPipeline)
EnemyThree = OrcBrute(CharacterSide.EnemySide, EventPipeline)

Allies: list[Character] = [AllyLeader, AllyTwo, AllyThree]
Enemies: list[Character] = [EnemyLeader, EnemyTwo, EnemyThree]

TurnManager = TurnManager(Allies, Enemies)

while True:

    CharacterInTurn = TurnManager.StartNextTurn()
    print("Turn: ", TurnManager.GetCurrentTurn())
    print("Character: ", CharacterInTurn.Name)
    print("Side: ", CharacterInTurn.Side.name + "\n")

    if CharacterInTurn.Side == CharacterSide.EnemySide:
        print("Skipping Enemy Turn\n")
        continue

    TargetAlly = -1
    TargetEnemy = -1

    Waiting = True
    while Waiting:

        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.constants.K_1:

                if Enemies[0].IsAlive:
                    TargetEnemy = 0
                    print("Currently Targeting: ", Enemies[TargetEnemy].Name)
                    print("Enemy Shield:", Enemies[TargetEnemy].GetCurrentShield())
                    print("Enemy Health:", Enemies[TargetEnemy].GetCurrentHealth(), "\n")

            if event.key == pygame.constants.K_2:

                if Enemies[1].IsAlive:
                    TargetEnemy = 1
                    print("Currently Targeting: ", Enemies[TargetEnemy].Name)
                    print("Enemy Shield:", Enemies[TargetEnemy].GetCurrentShield())
                    print("Enemy Health:", Enemies[TargetEnemy].GetCurrentHealth(), "\n")

            if event.key == pygame.constants.K_3:

                if Enemies[2].IsAlive:
                    TargetEnemy = 2
                    print("Currently Targeting: ", Enemies[TargetEnemy].Name)
                    print("Enemy Shield:", Enemies[TargetEnemy].GetCurrentShield())
                    print("Enemy Health:", Enemies[TargetEnemy].GetCurrentHealth(), "\n")

            if TargetEnemy != -1 and event.key == pygame.constants.K_b:
                CharacterInTurn.ActiveAbilities[0].Activate(Allies, Enemies, TargetAlly, TargetEnemy)
                print("Enemy Shield:", Enemies[TargetEnemy].GetCurrentShield())
                print("Enemy Health:", Enemies[TargetEnemy].GetCurrentHealth(), "\n")
                Waiting = False

            if TargetEnemy != -1 and event.key == pygame.constants.K_KP1:
                if len(CharacterInTurn.ActiveAbilities) > 1:
                    if CharacterInTurn.ActiveAbilities[1].TurnsToNextUse <= 0:
                        CharacterInTurn.ActiveAbilities[1].Activate(Allies, Enemies, TargetAlly, TargetEnemy)
                        Waiting = False
                    else:
                        print("Ability is on cooldown")

            if event.key == pygame.constants.K_SPACE:
                Waiting = False

    pygame.display.update()
    clock.tick(120)