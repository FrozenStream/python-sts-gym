from Entity import Entity
from Enemys import Enemy
from Cards import Card
import random
from CommandIO import human_chooseCard, human_chooseEntity, IOtype
from Powers import Power
from typing import Callable, Union
from collections import deque
import numpy as np


class CombatContext:
    def __init__(self, player: Entity, enemies: list[Enemy], draw_pile: list[Card], debug: bool = False):
        self.debug = debug
        self.actionQueue: deque[Callable[[CombatContext], None]] = deque()

        self.type: IOtype = IOtype.CHOOSE_CARD
        self.waiting: bool = False
        self.choice: np.ndarray = np.array([])

        self.player: Entity = player
        self.enemies: list[Enemy] = enemies
        self.turns = 0
        self.Energy = 0

        self.draw_pile: list[Card] = draw_pile
        self.hand: list[Card] = []
        self.discard_pile: list[Card] = []

        self.new_turn_flag: bool = True

        self.game_over_flag: bool = False
        self.player_win_flag: bool = False

    def debugPrint(self, msg: str, end: str = "\n"):
        if (self.debug): print(msg, end=end)

    def actionPush(self, action: Callable[['CombatContext'], None]):
        self.actionQueue.append(action)

    def actionPop(self) -> Callable[['CombatContext'], None]:
        return self.actionQueue.popleft()

    def needChoice(self, type: IOtype):
        self.waiting = True
        self.type = type
        self.debugPrint(f"Debug: Need choose {type.name}.")

    def getChoice(self) -> Union[Enemy, Card]:
        match self.type:
            case IOtype.CHOOSE_ENTITY:
                self.choice = np.argmax(self.choice[:len(self.enemies)])
                choice = self.enemies[self.choice]
            case IOtype.CHOOSE_DISCARD:
                self.choice = np.argmax(self.choice[:len(self.hand)])
                choice = self.hand[self.choice]
        self.debugPrint(f"Debug: Get choice {choice.name}.")
        self.type = IOtype.CHOOSE_CARD
        self.waiting = False
        return choice

    def checkEnd(self) -> bool:
        """
        检查是否结束游戏
        返回值：是否结束游戏
        """
        if (self.player.current_hp <= 0):
            self.debugPrint(f"Debug: Player {self.player.name} lost.")
            self.player_win_flag = False
            self.game_over_flag = True
        elif (all(enemy.OUT for enemy in self.enemies)):
            self.debugPrint("Debug: All enemies lost.")
            self.player_win_flag = True
            self.game_over_flag = True

    def enemys_turn(self) -> bool:
        """
        敌人回合
        返回值：是否结束游戏
        """
        for enemy in self.enemies:
            enemy.move(self, self.turns)
            if (self.checkEnd()): return True
        self.new_turn_flag = True
        return False

    def playerTurnBegin(self):
        """
        玩家回合开始
        """
        self.turns += 1
        self.Energy = 3
        clearShield(self, self.player)
        drawCards(self, 5)

    def human_step(self) -> bool:
        """
        玩家回合
        返回值：是否结束游戏
        """
        self.toNextState()
        if (self.game_over_flag): return True

        if (self.new_turn_flag):
            self.new_turn_flag = False
            self.playerTurnBegin()

        match self.type:
            case IOtype.CHOOSE_CARD:
                self.debugPrint(f"Debug: Player CHOOSE_CARD turn.")
                self.debugPrint(f"Debug: Current State:")
                self.debugPrint(f"Debug: Player HP: {self.player.current_hp}, Shield: {self.player.shield}")
                for enemy in self.enemies: self.debugPrint(f"Debug: Enemy {enemy.name} HP: {enemy.current_hp}, Shield: {enemy.shield}")

                choice: np.ndarray = human_chooseCard(self.hand)
                argmax = np.argmax(choice)                                          # =0: 结束回合, >0: 出牌
                if (argmax == 0):                                                   # 动作：结束回合
                    # 手牌全部弃置
                    for card in self.hand:
                        if (not card.is_ethereal): self.discard_pile.append(card)   # 非虚无牌加入弃牌堆
                    self.hand.clear()
                    self.enemys_turn()
                    if (self.game_over_flag): return True
                else:                                                               # 动作：出牌
                    card = self.hand[argmax - 1]
                    if (self.Energy >= card.cost):                                  # 执行卡牌动作
                        self.hand.remove(card)                                      # 从手牌中移除
                        self.Energy -= card.cost
                        for action in card.actions: self.actionPush(action)
                    if (not card.is_exhaust): self.discard_pile.append(card)        # 非消耗牌加入弃牌堆

            case IOtype.CHOOSE_ENTITY:
                self.choice: np.ndarray = human_chooseEntity(self.enemies)
                self.actionPop()(self)
                self.checkEnd()
                if (self.game_over_flag): return True

        return False

    def rl_step(self, action):
        """
        玩家回合
        返回值：是否结束游戏
        """
        self.toNextState()
        if (self.game_over_flag): return True

        if (self.new_turn_flag):
            self.new_turn_flag = False
            self.playerTurnBegin()

        match self.type:
            case IOtype.CHOOSE_CARD:
                self.debugPrint(f"Debug: Player CHOOSE_CARD turn.")
                self.debugPrint(f"Debug: Current State:")
                self.debugPrint(f"Debug: Player HP: {self.player.current_hp}, Shield: {self.player.shield}")
                for enemy in self.enemies: self.debugPrint(f"Debug: Enemy {enemy.name} HP: {enemy.current_hp}, Shield: {enemy.shield}")

                choice: np.ndarray = action
                argmax = np.argmax(choice)                                          # =0: 结束回合, >0: 出牌
                if (argmax == 0):                                                   # 动作：结束回合
                    # 手牌全部弃置
                    for card in self.hand:
                        if (not card.is_ethereal): self.discard_pile.append(card)   # 非虚无牌加入弃牌堆
                    self.hand.clear()
                    self.enemys_turn()
                    if (self.game_over_flag): return True
                else:                                                               # 动作：出牌
                    card = self.hand[argmax - 1]
                    if (self.Energy >= card.cost):                                  # 执行卡牌动作
                        self.hand.remove(card)                                      # 从手牌中移除
                        self.Energy -= card.cost
                        for action in card.actions: self.actionPush(action)
                    if (not card.is_exhaust): self.discard_pile.append(card)        # 非消耗牌加入弃牌堆

            case IOtype.CHOOSE_ENTITY:
                self.choice: np.ndarray = action
                self.actionPop()(self)
                self.checkEnd()
                if (self.game_over_flag): return True

        return False

    def toNextState(self):
        """
        切换到下一个等待状态
        """
        while (not self.waiting) and len(self.actionQueue) > 0:
            self.actionPop()(self)
            self.checkEnd()

    def rl_init(self):
        """
        初始化游戏
        """
        self.turns = 0
        self.Energy = 3
        self.new_turn_flag: bool = True


def hurtEntity(context: CombatContext, attacker: Entity, target: Entity, damage: int):
    target.receiveDamage(damage)


def attackEntity(context: CombatContext, attacker: Entity, target: Entity, damage: int):
    damage = bufferedDamage(context, attacker, damage)
    if (target.power_pool.getPower(Power.VULNERABLE) > 0):
        damage = int(damage * 1.5)
    target.receiveDamage(damage)
    thorns = target.power_pool.getPower(Power.THORNS)
    if (thorns > 0):
        hurtEntity(context, target, attacker, thorns)

    if (isinstance(target, Enemy) and target.current_hp <= 0):
        context.debugPrint(f"Debug: {target.name} died.")
        target.OUT = True


def getShield(context: CombatContext, target: Entity, shield: int):
    target.getShield(shield)


def healEntity(context: CombatContext, target: Entity, heal_amount: int):
    target.getHeal(heal_amount)


def getPower(context: CombatContext, target: Entity, power: int):
    target.power_pool.addPower(power, power)


def getEnergy(context: CombatContext, energy: int):
    context.Energy += energy


def reshuffleIntoDrawPile(context: CombatContext):
    for card in context.discard_pile:
        insertIndex = random.randint(0, len(context.draw_pile))
        context.draw_pile.insert(insertIndex, card)
    context.discard_pile.clear()


def drawCards(context: CombatContext, num: int):
    for _ in range(num):
        if (len(context.draw_pile) == 0):
            reshuffleIntoDrawPile(context)
        context.hand.append(context.draw_pile.pop())


def discardCard(context: CombatContext, card: Card):
    context.hand.remove(card)
    if (not card.is_ethereal):
        context.discard_pile.append(card)


def clearShield(context: CombatContext, target: Entity):
    target.clearShield()


def bufferedDamage(context: CombatContext, attacker: Entity, origin: int) -> int:
    damage = origin + attacker.power_pool.getPower(Power.STRENGTH)
    if (attacker.power_pool.getPower(Power.WEAK) > 0):
        damage = int(damage * 0.75)
    return damage
