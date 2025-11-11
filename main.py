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
while(not ctx.human_step()):
    pass
# gym = STS_Gym()
# gym.reset(ctx)
# state = gym.getState(ctx)

# while(not gym.checkStateEnd(state)):
#     action = gym.getAction(state)
#     gym.step(ctx, action)
#     state = gym.getState(ctx)
