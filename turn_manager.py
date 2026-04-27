from character import *

class TurnManager:
    Turn: int
    AllySide: list[Character]
    EnemySide: list[Character]
    TimeMin: float

    def __init__(self, AllySide: list[Character], EnemySide: list[Character]):

        self.Turn = 0
        self.AllySide = AllySide
        self.EnemySide = EnemySide
        self.TimeMin = -1

    def StartNextTurn(self):

        self.Turn = self.Turn + 1

        AllyTTT: list[float] = []
        EnemyTTT: list[float] = []

        for character in self.AllySide:
            TimeToTurn = (1 - character.GetTurnMeter()) / character.GetCurrentSpeed()
            AllyTTT.append(TimeToTurn)

        for character in self.EnemySide:
            TimeToTurn = (1 - character.GetTurnMeter()) / character.GetCurrentSpeed()
            EnemyTTT.append(TimeToTurn)

        ClosestAllyTime = min(AllyTTT)
        ClosestEnemyTime = min(EnemyTTT)

        if ClosestAllyTime <= ClosestEnemyTime:
            self.TimeMin = ClosestAllyTime
        else:
            self.TimeMin = ClosestEnemyTime

        for character in self.AllySide:
            character.ModifyTurnMeter(character.GetCurrentSpeed() * self.TimeMin)

            if character.GetTurnMeter() > 1.0:
                character.SetTurnMeter(1.0)

        for character in self.EnemySide:
            character.ModifyTurnMeter(character.GetCurrentSpeed() * self.TimeMin)

            if character.GetTurnMeter() > 1.0:
                character.SetTurnMeter(1.0)

        for character in self.AllySide:
            if character.GetTurnMeter() >= 0.999:
                character.SetTurnMeter(0.0)
                return character

        for character in self.EnemySide:
            if character.GetTurnMeter() >= 0.999:
                character.SetTurnMeter(0.0)
                return character

        return None

    def GetCurrentTurn(self):
        return self.Turn