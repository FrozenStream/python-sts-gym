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
]


ctx = CombatContext(player, enemy, cards, debug=True)
ctx.Move()
