from CombatContext import CombatContext
import numpy as np
from CommandIO import IOtype
from Cards import Card




class STS_Gym:
    def __init__(self, context: CombatContext):
        pass

    def step(self, context: CombatContext, action: np.ndarray):
        match context.ActionType:
            case IOtype.CHOOSE_CARD:
                card:Card = context.hand[0]
                context.PlayCard(card)
            case IOtype.CHOOSE_ENTITY:
                pass
            case IOtype.END_TURN:
                pass


    def reset(self, context: CombatContext):
        self.context = CombatContext()

    def getState(self, context: CombatContext) -> str:
        cur_hp = context.player.current_hp
        max_hp = context.player.max_hp
        cur_shield = context.player.shield

        enemies = [
            (enemy.current_hp, enemy.max_hp, enemy.shield)
            for enemy in context.enemies
        ]
        pass
