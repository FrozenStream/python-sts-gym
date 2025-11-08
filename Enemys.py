from Entity import Entity
from CombatContext import *
from typing import Callable, Tuple
from Powers import Power


class Enemy(Entity):
    """敌人基类"""

    def __init__(self, name: str, max_hp: int):
        super().__init__(name, max_hp)
        self.max_hp = max_hp
        self.current_hp = max_hp

        self.OUT = False

    def InitActions(self, actions: Tuple[Tuple[Callable[[CombatContext], None], ...], ...]):
        self.actions = actions

    def move(self, context: CombatContext):
        num = context.turns % len(self.actions)
        for action in self.actions[num]:
            action(context)


def createJawWorm() -> Enemy:
    MaxHP = 100
    Jaw_Worm = Enemy('Jaw Worm', MaxHP)
    Powers = (
        (Power.STRENGTH, 0),
    )
    Actions = (
        (
            lambda context: attackEntity(context, Jaw_Worm, context.player, 8),
        ),
        (
            lambda context: attackEntity(context, Jaw_Worm, context.player, 4),
            lambda context: getShield(context, Jaw_Worm, 6),
        ),
    )
    for power, amount in Powers:
        Jaw_Worm.InitPower(power, amount)
    Jaw_Worm.InitActions(Actions)
    return Jaw_Worm
