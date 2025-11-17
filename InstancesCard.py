from Cards import Card, CardType
from CombatContext import *
from typing import Callable, Tuple, Dict

CardLambdas: Dict[str, Tuple[Callable[[CombatContext], None], ...]] = {
    'attack': (
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackEntity(context, context.player, context.getChoice(), 6),
    ),
    'defend': (
        lambda context: gainShield(context, context.player, 6),
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

