from Entity import Entity, Player, Enemy
from Cards import Card
from Powers import Power
import random
from CommandIO import IOtype
from typing import Callable, Union
from collections import deque
import numpy as np


class CombatContext:
    def __init__(self, player: Player, enemies: list[Enemy], draw_pile: list[Card], debug: bool = False):
        self.debug = debug
        self.action_queue: deque[Callable[[CombatContext], None]] = deque()

        self.io_type: IOtype = IOtype.CHOOSE_CARD
        self.waiting: bool = False
        self.choice: Union[Enemy, Card] = None

        self.player: Player = player
        self.enemies: list[Enemy] = enemies
        self.turns = 0
        self.energy = 0

        self.draw_pile: list[Card] = draw_pile
        random.shuffle(self.draw_pile)
        self.hand: list[Card] = []
        self.discard_pile: list[Card] = []

        self.new_turn_flag: bool = True

        self.game_over_flag: bool = False
        self.player_win_flag: bool = False

    def debugPrint(self, msg: str, end: str = "\n"):
        if (self.debug): print(msg, end=end)

    def actionPush(self, action: Callable[['CombatContext'], None]):
        self.action_queue.append(action)

    def actionPop(self) -> Callable[['CombatContext'], None]:
        return self.action_queue.popleft()

    def howManyLivingEnemies(self) -> int:
        return sum(not enemy.OUT for enemy in self.enemies)

    def needChoice(self, IOtype: IOtype):
        self.waiting = True
        self.io_type = IOtype
        self.debugPrint(f"Debug: Need choose {IOtype.name}.")

    def getChoice(self) -> Union[Enemy, Card]:
        self.debugPrint(f"Debug: Get choice {self.choice.name}.")
        self.io_type = IOtype.CHOOSE_CARD
        self.waiting = False
        return self.choice

    def checkEnd(self) -> bool:
        """
        检查是否结束游戏
        返回值：是否结束游戏
        """
        if (self.player.OUT):
            self.debugPrint("Debug: Player lost.")
            self.player_win_flag = False
            self.game_over_flag = True
        elif (all(enemy.OUT for enemy in self.enemies)):
            self.debugPrint("Debug: All enemies lost.")
            self.player_win_flag = True
            self.game_over_flag = True

    def playerTurnBegin(self):
        """
        玩家回合开始
        """
        self.turns += 1
        self.energy = 3
        EntityBeginTurn(self, self.player)
        drawCards(self, 5)

    def playerTurnEnd(self):
        """
        玩家回合结束
        """
        # 手牌全部弃置
        left_card = []
        for card in self.hand:
            if (not card.is_ethereal): self.discard_pile.append(card)   # 非虚无牌加入弃牌堆
            if (card.is_retain): left_card.append(card)                 # 保留牌留在手牌
        self.hand = left_card

        # 敌人回合
        for enemy in self.enemies: EntityBeginTurn(self, enemy)
        for enemy in self.enemies:
            enemy.move(self, self.turns, self.debugPrint)
            if self.checkEnd(): return
        self.new_turn_flag = True

    def step(self, action):
        """
        玩家回合
        返回值：是否结束游戏
        """
        self.toNextState()
        if (self.game_over_flag): return True

        match self.io_type:
            case IOtype.CHOOSE_CARD:
                argmax = np.argmax(action)                                          # =0: 结束回合, >0: 出牌
                if (argmax == 0):                                                   # 动作：结束回合
                    self.playerTurnEnd()
                    if (self.game_over_flag): return True
                else:                                                               # 动作：出牌
                    card = self.hand[argmax - 1]
                    if (self.energy >= card.cost):                                  # 执行卡牌动作
                        self.hand.remove(card)                                      # 从手牌中移除
                        self.energy -= card.cost
                        for action in card.actions: self.actionPush(action)
                    if (not card.is_exhaust): self.discard_pile.append(card)        # 非消耗牌加入弃牌堆

            case IOtype.CHOOSE_ENTITY:
                argmax = np.argmax(action[:len(self.enemies)])
                self.choice: Enemy = self.enemies[argmax]
                self.actionPop()(self)
                self.checkEnd()
                if (self.game_over_flag): return True

            case IOtype.CHOOSE_DISCARD:
                argmax = np.argmax(action[:len(self.hand)])
                self.choice: Card = self.hand[argmax]
                self.actionPop()(self)
                self.checkEnd()
                if (self.game_over_flag): return True

        return False

    def toNextState(self):
        """
        切换到下一个等待状态
        """
        while (not self.waiting) and len(self.action_queue) > 0:
            self.actionPop()(self)
            self.checkEnd()
        if (self.game_over_flag): return

        if (self.new_turn_flag):
            self.new_turn_flag = False
            self.playerTurnBegin()

    def DebugPrintState(self):
        """
        打印当前状态
        """
        self.debugPrint(f"Debug: Current Energy: {self.energy}")
        self.debugPrint(f"Debug: Player HP: {self.player.current_hp}, Shield: {self.player.shield}")
        for enemy in self.enemies: 
            self.debugPrint(f"Debug: Enemy {enemy.name} HP: {enemy.current_hp}, Shield: {enemy.shield}, Power: {enemy.power_pool.displayPower()}")


def hurtEntity(context: CombatContext, attacker: Entity, target: Entity, damage: int):
    '''
    attacker deal damage to target without considering chain reaction.
    '''
    target.receiveDamage(damage)


def attackEntity(context: CombatContext, attacker: Entity, target: Entity, damage: int, times: int):
    '''
    attacker deal damage to target with considering chain reaction.
    '''
    damage = bufferedDamage(context, attacker, damage)
    for _ in range(times):
        if (target.power_pool.getPower(Power.VULNERABLE) > 0): damage = int(damage * 1.5)  # 易伤
        target.receiveDamage(damage)
        # 荆棘
        if (target.power_pool.getPower(Power.THORNS) > 0):
            hurtEntity(context, target, attacker, target.power_pool.getPower(Power.THORNS))

def attackAllEntity(context: CombatContext, attacker: Entity, targets: list[Entity], damage: int, times: int):
    '''
    attacker deal damage to all targets with considering chain reaction.
    '''
    damage = bufferedDamage(context, attacker, damage)
    for _ in range(times):
        for target in targets:
            if (target.OUT): continue
            if (target.power_pool.getPower(Power.VULNERABLE) > 0): damage = int(damage * 1.5)  # 易伤
            target.receiveDamage(damage)
            # 荆棘
            if (target.power_pool.getPower(Power.THORNS) > 0):
                hurtEntity(context, target, attacker, target.power_pool.getPower(Power.THORNS))

def randomAttackEntity(context: CombatContext, attacker: Entity, targets: list[Entity], damage: int, times: int):
    damage = bufferedDamage(context, attacker, damage)
    for _ in range(times):
        target = random.choice(targets)
        if (target.power_pool.getPower(Power.VULNERABLE) > 0): damage = int(damage * 1.5)  # 易伤
        target.receiveDamage(damage)
        # 荆棘
        if (target.power_pool.getPower(Power.THORNS) > 0):
            hurtEntity(context, target, attacker, target.power_pool.getPower(Power.THORNS))


def gainShield(context: CombatContext, target: Entity, shield: int):
    shield += target.power_pool.getPower(Power.DEXTERITY)  # 敏捷
    if (target.power_pool.getPower(Power.FRAGILE) > 0): shield *= 0.75  # 脆弱
    target.getShield(shield)


def addShield(context: CombatContext, target: Entity, shield: int):
    target.getShield(shield)


def healEntity(context: CombatContext, target: Entity, heal_amount: int):
    target.getHeal(heal_amount)


def entityGainPower(context: CombatContext, target: Entity, power: Power, amount: int):
    target.power_pool.addPower(power, amount)

def allEntityGainPower(context: CombatContext, targets: list[Entity], power: Power, amount: int):
    for target in targets:
        entityGainPower(context, target, power, amount)


def gainEnergy(context: CombatContext, energy: int):
    context.energy += energy


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


def addCardToPile(context: CombatContext, card: Card, pile: list[Card]):
    pile.append(card)


def bufferedDamage(context: CombatContext, attacker: Entity, origin: int) -> int:
    damage = origin + attacker.power_pool.getPower(Power.STRENGTH)  # 力量
    if (attacker.power_pool.getPower(Power.WEAK) > 0): damage = int(damage * 0.75)  # 虚弱
    return damage


def EntityBeginTurn(context: CombatContext, target: Entity):
    if (target.OUT): return
    target.clearShield()
    # 金属化
    if (target.power_pool.getPower(Power.METALLICIZE) > 0):
        gainShield(context, target, target.power_pool.getPower(Power.METALLICIZE))


def countStrike(context: CombatContext) -> int:
    count = 0
    for card in context.hand:
        if ('Strike' in card.name): count += 1
    return count
