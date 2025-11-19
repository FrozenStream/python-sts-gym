from Powers import Power, PowerPool
from typing import Callable

class Entity():
    """实体基类"""

    def __init__(self, name: str, max_hp: int):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.power_pool = PowerPool()
        self.shield = 0

        self.OUT: bool = False

    def InitPower(self, power: Power, amount: int):
        self.power_pool.addPower(power, amount)

    def getHeal(self, heal: int):
        self.current_hp = min(self.max_hp, self.current_hp + heal)

    def getShield(self, shield: int):
        self.shield += shield
        self.shield = min(self.shield, 999)

    def damageShield(self, damage: int):
        self.shield -= min(self.shield, damage)

    def clearShield(self):
        self.shield = 0

    def getHurt(self, damage: int):
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.current_hp = 0
            self.OUT = True

    def receiveDamage(self, damage: int):
        if (self.shield >= damage):
            self.damageShield(damage)
        else:
            tmp = self.shield
            self.damageShield(tmp)
            self.getHurt(damage - tmp)


class Player(Entity):
    def __init__(self, name: str, max_hp: int = 80):
        super().__init__(name, max_hp)


class Enemy(Entity):
    def __init__(self, name: str, max_hp):
        super().__init__(name, max_hp)

    def move(self, context, turns: int, debugPrint: Callable[[str], None]):
        pass
