from Entity import Enemy
from Powers import Power
from CombatContext import *



class JawWorm(Enemy):
    def __init__(self, max_hp: int = 10):
        super().__init__('Jaw Worm', max_hp)
    
    def move(self, context: CombatContext, turns: int):
        if self.OUT: return
        if turns % 2 == 0:
            attackEntity(context, self, context.player, 8)
        else:
            attackEntity(context, self, context.player, 4)
            gainShield(context, self, 6)
