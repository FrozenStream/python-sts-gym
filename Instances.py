from Cards import Card, CardType
from CombatContext import *
from Powers import Power
from Enemys import Enemy
from typing import Callable, Tuple, Dict

CardLambdas: Dict[str, Tuple[Callable[[CombatContext], None], ...]] = {
    'attack': (
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackEntity(context, context.player, context.getChoice(), 6),
    ),
    'defend': (
        lambda context: getShield(context, context.player, 6),
    ),
    'bowlingBash': (
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackEntity(context, context.player, context.getChoice(), 6 * context.howManyLivingEnemies()),
    ),
    'prepared': (
        lambda context: drawCards(context, 1),
        lambda context: context.needChoice(IOtype.CHOOSE_DISCARD),
        lambda context: discardCard(context, context.getChoice()),
    ),

}

attack = Card('attack', 1, CardType.ATTACK, CardLambdas['attack'])
defend = Card('defend', 1, CardType.SKILL, CardLambdas['defend'])
bowlingBash = Card('bowlingBash', 1, CardType.ATTACK, CardLambdas['bowlingBash'])
prepared = Card('prepared', 1, CardType.SKILL, CardLambdas['prepared'])


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
    for power, amount in Powers: Jaw_Worm.InitPower(power, amount)
    Jaw_Worm.InitActions(actions_lambda)
    return Jaw_Worm
