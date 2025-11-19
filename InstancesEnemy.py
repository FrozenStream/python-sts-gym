from Entity import Enemy
from Powers import Power
from CombatContext import *



class JawWorm(Enemy):
    def __init__(self, max_hp: int = 20):
        super().__init__('Jaw Worm', max_hp)
    
    def move(self, context: CombatContext, turns: int, debugPrint: Callable[[str], None]):
        if self.OUT: return
        if turns % 2 == 0:
            attackEntity(context, self, context.player, 8, 1)
        else:
            attackEntity(context, self, context.player, 4, 1)
            gainShield(context, self, 6)
