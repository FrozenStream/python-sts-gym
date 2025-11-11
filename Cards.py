from typing import Callable, Tuple


class Card():
    """卡牌基类"""

    def __init__(self, name: str, is_exhaust: bool, is_retain: bool, is_ethereal: bool, cost: int, actions: Tuple[Callable, ...]):
        self.name = name
        self.is_exhaust = is_exhaust
        self.is_retain = is_retain
        self.is_ethereal = is_ethereal
        self.cost = cost
        self.actions = actions
