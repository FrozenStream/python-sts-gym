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