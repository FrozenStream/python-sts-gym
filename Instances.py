from Cards import Card
from CombatContext import *
from Powers import Power
from Enemys import Enemy
from typing import Callable, Tuple

attack_lambda: Callable[[CombatContext], None] = lambda context: (
    attackEntity(context, context.player, context.changeActionType(IOtype.CHOOSE_ENTITY), 6),
)

attack = Card('attack', False, False, False, 1, attack_lambda)


defend_lambda: Callable[[CombatContext], None] = lambda context: (
    getShield(context, context.player, 6)
)
defend = Card('defend', False, False, False, 1, defend_lambda)


def createJawWorm() -> Enemy:
    MaxHP = 10
    Jaw_Worm = Enemy('Jaw Worm', MaxHP)
    Powers = (
        (Power.STRENGTH, 0),
    )
    actions_lambda: Tuple[Callable[[CombatContext], None], ...] = (
        lambda context: (
            attackEntity(context, Jaw_Worm, context.player, 8),
        ),
        lambda context: (
            attackEntity(context, Jaw_Worm, context.player, 4),
            getShield(context, Jaw_Worm, 6),
        ),
    )
    for power, amount in Powers:
        Jaw_Worm.InitPower(power, amount)
    Jaw_Worm.InitActions(actions_lambda)
    return Jaw_Worm
