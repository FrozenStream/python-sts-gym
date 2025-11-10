from Entity import Entity
from typing import Callable, Tuple


class Enemy(Entity):
    """敌人基类"""

    def __init__(self, name: str, max_hp: int):
        super().__init__(name, max_hp)
        self.max_hp = max_hp
        self.current_hp = max_hp

        self.OUT = False

    def InitActions(self, actions: Tuple[Callable, ...]):
        self.actions = actions

    def move(self, context, turn_num: int):
        num = (turn_num - 1) % len(self.actions)
        for action in self.actions[num]:
            action(context)
