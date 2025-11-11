import numpy as np
from enum import Enum
from Entity import Entity
from Cards import Card

class IOtype(Enum):
    CHOOSE_CARD = 0
    CHOOSE_ENTITY = 1
    CHOOSE_DISCARD = 2


def human_chooseEntity(Entitys: list[Entity]) -> np.ndarray:
    """选择实体"""
    print('Debug: Please choose an entity.')
    for i, entity in enumerate(Entitys):
        print(f'{i}: {entity.name}')
    choice = int(input())

    ans = np.array([0] * 11)
    ans[choice] = 1
    return ans


def human_chooseCard(hand: list[Card]) -> np.ndarray:
    """选择卡牌"""
    print('Debug: Please choose a card.')
    print('0: End your turn')
    for i, card in enumerate(hand):
        print(f'{i + 1}: {card.name} Cost: {card.cost}')
    choice = int(input())
    ans = np.array([0] * 11)
    ans[choice] = 1
    return ans
