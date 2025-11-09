import numpy as np


def chooseEntity(Entitys: list):
    """选择实体"""
    print('请选择实体：')
    choice = int(input())
    return Entitys[choice]


def chooseCard(hand: list):
    """选择卡牌"""
    choice = int(input())
    return hand[choice]


def endTurn() -> bool:
    """
    结束回合
    返回值：是否结束游戏
    """
    print('是否结束回合？(0: 否, 1: 是)')
    choice = int(input())
    return choice == 1

