from enum import Enum


class Power(Enum):
    STRENGTH = 0  # 力量
    DEXTERITY = 1  # 敏捷
    METALLICIZE = 2  # 金属化
    THORNS = 3  # 荆棘
    WEAK = 4  # 虚弱
    VULNERABLE = 5  # 易伤
    FRAGILE = 6  # 脆弱



class PowerPool():
    _powers: list[int] = [0] * len(Power)

    def getPower(self, power: Power) -> int:
        return self._powers[power.value]

    def addPower(self, power: Power, amount: int):
        self._powers[power.value] += amount
