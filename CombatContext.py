from Enemys import Enemy
from Player import Player
from Entity import Entity
from Cards import Card
import random
from CommandIO import chooseCard, endTurn


class CombatContext:
    def __init__(self, player, enemies, draw_pile: list[Card], debug: bool = False):
        self.debug = debug

        self.player: Player = player
        self.enemies: list[Enemy] = enemies

        self.turns = 0
        self.Cost = 0

        self.draw_pile: list[Card] = draw_pile
        self.hand: list[Card] = []
        self.discard_pile: list[Card] = []

    def debugPrint(self, msg: str):
        if (self.debug):
            print(msg)

    def checkEnd(self) -> bool:
        """
        检查是否结束游戏
        返回值：是否结束游戏
        """
        end: bool = False
        if (self.player.current_hp <= 0):
            self.debugPrint(f"Debug: Player {self.player.name} died.")
            end = True
        if (all(enemy.OUT for enemy in self.enemies)):
            self.debugPrint("Debug: All enemies died.")
            end = True
        if (end):
            self.debugPrint(f"Debug: Player {self.player.name} won.")
        else:
            self.debugPrint(f"Debug: Player {self.player.name} lost.")
        return end

    def PlayCard(self):
        card: Card = chooseCard(self)
        card.play(self)

        if (not card.is_exhaust):
            self.discard_pile.append(card)

    def enemys_turn(self) -> bool:
        """
        敌人回合
        返回值：是否结束游戏
        """
        for enemy in self.enemies:
            enemy.move(self)
            self.debugPrint(f"Debug: {enemy.name} moved.")
            if (self.checkEnd()): return True
            
        return False

    def player_turn(self) -> bool:
        """
        玩家回合
        返回值：是否结束游戏
        """
        self.turns += 1
        self.Cost = 3

        drawCards(self, 5)
        while (True):
            # self.UsePotion()
            # 出牌阶段
            self.PlayCard()
            if (self.checkEnd()):
                return True
            # 判断回合结束
            if (endTurn(self)):
                break

        # 手牌全部弃置
        for card in self.hand:
            if (not card.is_ethereal):
                self.discard_pile.append(card)
        self.hand.clear()

        return False

    def Move(self):
        while (True):
            self.player_turn()
            self.enemys_turn()


def hurtEntity(context: CombatContext, attacker: Entity, target: Entity, damage: int):
    target.receiveDamage(damage)


def attackEntity(context: CombatContext, attacker: Entity, target: Entity, damage: int):
    damage = bufferedDamage(context, attacker, damage)
    target.receiveDamage(damage)
    thorns = target.power_pool.thorns
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


def getCost(context: CombatContext, cost: int):
    context.Cost += cost


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


def bufferedDamage(context: CombatContext, attacker: Entity, origin: int) -> int:
    damage = origin+attacker.power_pool.strength
    if (attacker.power_pool.weak > 0):
        damage = int(damage*0.75)
    return damage
