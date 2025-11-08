from CombatContext import CombatContext
from Entity import Entity
import numpy as np
from Cards import Card


def chooseEntity(context: CombatContext) -> Entity:
    """选择实体"""
    print('请选择实体：')
    choice = int(input())
    if choice == 0:
        return context.player
    else:
        return context.enemies[choice-1]
    

def chooseCard(context: CombatContext) -> Card:
    """选择卡牌"""
    print('请选择卡牌：')
    choice = int(input())
    return context.hand[choice]


def endTurn(context: CombatContext) -> bool:
    """
    结束回合
    返回值：是否结束游戏
    """
    if (context.player.current_hp <= 0):
        return True
    for enemy in context.enemies:
        if (enemy.current_hp <= 0):
            return True
    return False



class CombatState:
    """游戏状态类"""
    def __init__(self, context: CombatContext):
        self.context = context
        self.turns = context.turns
        self.current_hp = context.player.current_hp
        self.max_hp = context.player.max_hp
        self.shield = context.player.shield
        self.powers = context.player.power_pool._powers

    def getVec(self) -> np.ndarray:
        """获取状态向量"""
        return np.array([self.turns, self.current_hp, self.max_hp, self.shield] + self.powers, dtype=np.float32)

    def getReward(self) -> float:
        """获取奖励"""
        reward = 0
        reward += self.current_hp / self.max_hp
        return reward


def getCombatState(context: CombatContext) -> np.ndarray:
    """
    获取当前游戏状态，供强化学习代理使用
    返回一个数值数组表示当前游戏状态
    """
    state: CombatState = CombatState(context)
    
    # 添加敌人信息
    for enemy in context.enemies:
        state.append(enemy.current_hp / enemy.max_hp)  # 敌人血量比例
        state.append(enemy.shield)  # 敌人护盾值
        
        # 添加敌人效果信息
        for i in range(len(enemy.power_pool._powers)):
            state.append(enemy.power_pool._powers[i])
    
    # 如果敌人数量不足，用0填充
    max_enemies = 3  # 假设最多同时战斗3个敌人
    while len(context.enemies) < max_enemies:
        # 血量比例、护盾值和效果信息都用0填充
        state.extend([0] * (2 + len(context.player.power_pool._powers)))
    
    return np.array(state, dtype=np.float32)
