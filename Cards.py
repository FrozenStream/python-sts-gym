from abc import abstractmethod
from CombatContext import *
from typing import Callable, Tuple
from CommandIO import *


class Card():
    """卡牌基类"""

    def __init__(self, name: str, is_exhaust: bool, is_retain: bool, is_ethereal: bool, actions: Tuple[Callable[[CombatContext], None], ...]):
        self.name = name
        self.is_exhaust = is_exhaust
        self.is_retain = is_retain
        self.is_ethereal = is_ethereal
        self.actions = actions

    @abstractmethod
    def play(self, combatContext: CombatContext):
        for action in self.actions:
            action(combatContext)


attack = Card('attack', False, False, False,
              (lambda context: attackEntity(
                  context, context.player, chooseEntity(context), 6),))


defend = Card('defend', False, False, False,
              (lambda context: getShield(context, context.player, 6),))
