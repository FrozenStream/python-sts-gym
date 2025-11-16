from CombatContext import CombatContext
import Player
from Instances import *
from Cards import *

player = Player.Player('Player', 80)
enemy = [
    createJawWorm(),
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
    ctx.human_step()
