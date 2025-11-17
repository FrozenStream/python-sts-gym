from CombatContext import CombatContext
from Entity import Entity, Player, Enemy
from InstancesCard import *
from InstancesEnemy import *
from Cards import *
from CommandIO import *

player = Player('Player', 80)
enemy = [
    JawWorm(),
    JawWorm(),
    JawWorm(),
    JawWorm(),
]

cards = [
    attack,
    attack,
    attack,
    attack,
    defend,
    defend,
    defend,
    defend,
    prepared,
]


ctx = CombatContext(player, enemy, cards, debug=True)
while(not ctx.game_over_flag):
    ctx.toNextState()
    ctx.DebugPrintState()
    match ctx.type:
        case IOtype.CHOOSE_CARD: input = human_chooseCard(ctx.hand)
        case IOtype.CHOOSE_ENTITY: input = human_chooseEntity(ctx.enemies)
        case IOtype.CHOOSE_DISCARD: input = human_chooseDiscard(ctx.hand)
    ctx.step(input)
