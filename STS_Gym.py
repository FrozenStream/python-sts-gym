from CombatContext import CombatContext
import numpy as np
from CommandIO import IOtype
from Cards import Card




class STS_Gym:
    def __init__(self):
        pass

    def step(self, context: CombatContext, action: np.ndarray):
        context.rl_step(action)
        

    def reset(self, context: CombatContext):
        self.context = CombatContext()

    def getState(self, context: CombatContext) -> np.ndarray:
        context.toNextState()
        cur_hp = context.player.current_hp
        max_hp = context.player.max_hp
        cur_shield = context.player.shield

        enemies = [
            (enemy.current_hp, enemy.max_hp, enemy.shield)
            for enemy in context.enemies
        ]

        is_end = context.game_over_flag
        pass


    def getAction(self, state: np.ndarray) -> np.ndarray:
        pass

