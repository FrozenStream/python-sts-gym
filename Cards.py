from typing import Callable, Tuple


from enum import Enum


class CardType(Enum):
    ATTACK = 1
    SKILL = 2
    POWER = 3
    STATUS = 4
    CURSE = 5


class Card():
    """卡牌基类"""

    def __init__(self, name: str, cost: int, card_type: CardType, actions: Tuple[Callable, ...],
                 is_exhaust: bool = False, is_retain: bool = False, is_ethereal: bool = False
                 ):
        self.name = name
        self.cost = cost
        self.card_type = card_type
        self.actions = actions
        self.is_exhaust = is_exhaust
        self.is_retain = is_retain
        self.is_ethereal = is_ethereal
