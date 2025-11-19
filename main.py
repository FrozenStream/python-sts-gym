from CombatContext import CombatContext
from Entity import Player
from InstancesCard import *
from InstancesEnemy import *
from CommandIO import *

player = Player('Player', 80)
enemy = [
    JawWorm(),
    JawWorm(),
    JawWorm(),
]

cards = [
    Strike_red,
    Strike_red,
    Defend_red,
    Defend_red,
    Dash,
    Dropkick,
]


ctx = CombatContext(player, enemy, cards, debug=True)
while not ctx.game_over_flag:
    ctx.toNextState()
    ctx.DebugPrintState()
    match ctx.io_type:
        case IOtype.CHOOSE_CARD: step = human_chooseCard(ctx.hand)
        case IOtype.CHOOSE_ENTITY: step = human_chooseEntity(ctx.enemies)
        case IOtype.CHOOSE_DISCARD: step = human_chooseDiscard(ctx.hand)
    ctx.step(step)
