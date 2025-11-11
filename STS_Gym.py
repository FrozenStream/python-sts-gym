from CombatContext import CombatContext
import numpy as np
from CommandIO import IOtype
from Cards import Card




class STS_Gym:
    def __init__(self):
        pass

    def step(self, context: CombatContext, action: np.ndarray):
        game_end = context.rl_step(action)
        game_end = game_end or context.toNextState()
        
        if(game_end): return context.player_win_flag

    def reset(self, context: CombatContext):
        self.context = CombatContext()

    def getState(self, context: CombatContext) -> np.ndarray:
        cur_hp = context.player.current_hp
        max_hp = context.player.max_hp
        cur_shield = context.player.shield

        enemies = [
            (enemy.current_hp, enemy.max_hp, enemy.shield)
            for enemy in context.enemies
        ]

        is_end = context.is_end
        pass


    def getAction(self, state: np.ndarray) -> np.ndarray:
        pass

