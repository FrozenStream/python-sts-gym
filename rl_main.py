from CombatContext import CombatContext
import Player
from Instances import *
from Cards import *
from STS_Gym import STS_Gym

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
gym = STS_Gym()
gym.reset(ctx)
while(True):
    game_end = ctx.toNextState()
    
    state = gym.getState(ctx)
    pass