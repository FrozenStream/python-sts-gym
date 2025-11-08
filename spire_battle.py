import random
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional


class CardType(Enum):
    ATTACK = "attack"
    SKILL = "skill"
    POWER = "power"


class Card(ABC):
    """卡牌基类"""
    def __init__(self, name: str, cost: int, card_type: CardType):
        self.name = name
        self.cost = cost
        self.card_type = card_type

    @abstractmethod
    def play(self, player, targets: List['Enemy']):
        """使用卡牌"""
        pass

    def __str__(self):
        return f"{self.name}(cost: {self.cost})"


class AttackCard(Card):
    """攻击卡"""
    def __init__(self, name: str, cost: int, damage: int):
        super().__init__(name, cost, CardType.ATTACK)
        self.damage = damage

    def play(self, player, targets: List['Enemy']):
        if targets:
            target = targets[0]  # 默认攻击第一个敌人
            target.take_damage(self.damage)
            print(f"{player.name} 使用 {self.name} 对 {target.name} 造成 {self.damage} 点伤害!")


class SkillCard(Card):
    """技能卡"""
    def __init__(self, name: str, cost: int, block: int = 0, heal: int = 0):
        super().__init__(name, cost, CardType.SKILL)
        self.block = block
        self.heal = heal

    def play(self, player, targets: List['Enemy']):
        if self.block > 0:
            player.gain_block(self.block)
            print(f"{player.name} 使用 {self.name} 获得 {self.block} 点格挡!")
        
        if self.heal > 0:
            player.heal(self.heal)
            print(f"{player.name} 使用 {self.name} 恢复 {self.heal} 点生命!")


class Entity:
    """实体基类（玩家和敌人的共同属性）"""
    def __init__(self, name: str, max_hp: int):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.block = 0

    def take_damage(self, damage: int):
        # 先扣除格挡
        if self.block >= damage:
            self.block -= damage
            damage = 0
        else:
            damage -= self.block
            self.block = 0
        
        # 扣除生命值
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
    
    def heal(self, amount: int):
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

    def is_dead(self):
        return self.current_hp <= 0


class Player(Entity):
    """玩家类"""
    def __init__(self, name: str, max_hp: int):
        super().__init__(name, max_hp)
        self.energy = 0
        self.max_energy = 3
        self.deck: List[Card] = []
        self.hand: List[Card] = []
        self.discard_pile: List[Card] = []
        self.draw_pile: List[Card] = []

    def gain_block(self, block: int):
        self.block += block

    def gain_energy(self, amount: int = None):
        """获取能量"""
        if amount is None:
            self.energy = self.max_energy  # 新回合开始时恢复到最大值
        else:
            self.energy += amount
            if self.energy > self.max_energy:
                self.energy = self.max_energy

    def draw_cards(self, count: int = 5):
        """抽牌"""
        # 如果抽牌堆为空，则将弃牌堆洗牌后放入抽牌堆
        if len(self.draw_pile) < count:
            self.draw_pile.extend(self.discard_pile)
            self.discard_pile.clear()
            random.shuffle(self.draw_pile)
        
        # 抽牌
        drawn = min(count, len(self.draw_pile))
        for _ in range(drawn):
            if self.draw_pile:
                card = self.draw_pile.pop()
                self.hand.append(card)
        
        return drawn

    def play_card(self, card_index: int, targets: List['Enemy']):
        """打出一张牌"""
        if 0 <= card_index < len(self.hand):
            card = self.hand[card_index]
            if card.cost <= self.energy:
                self.energy -= card.cost
                card.play(self, targets)
                self.hand.pop(card_index)
                self.discard_pile.append(card)
                return True
            else:
                print("能量不足!")
                return False
        else:
            print("无效的手牌索引!")
            return False

    def start_turn(self):
        """开始回合"""
        self.gain_energy()  # 恢复能量
        self.draw_cards()   # 抽牌

    def end_turn(self):
        """结束回合"""
        # 将手牌放入弃牌堆
        self.discard_pile.extend(self.hand)
        self.hand.clear()


class Enemy(Entity):
    """敌人基类"""
    def __init__(self, name: str, max_hp: int, intent: str = "attack"):
        super().__init__(name, max_hp)
        self.intent = intent  # 敌人意图

    def take_turn(self, player: Player):
        """敌人行动"""
        if self.intent == "attack":
            damage = random.randint(5, 10)  # 随机伤害
            player.take_damage(damage)
            print(f"{self.name} 攻击 {player.name} 造成 {damage} 点伤害!")


class Battle:
    """战斗系统"""
    def __init__(self, player: Player, enemies: List[Enemy]):
        self.player = player
        self.enemies = enemies

    def is_battle_over(self):
        """检查战斗是否结束"""
        # 玩家死亡
        if self.player.is_dead():
            return True, "lose"
        
        # 所有敌人都死亡
        if all(enemy.is_dead() for enemy in self.enemies):
            return True, "win"
        
        return False, ""

    def display_state(self):
        """显示当前状态"""
        print("\n=== 当前状态 ===")
        print(f"{self.player.name}: HP {self.player.current_hp}/{self.player.max_hp}, "
              f"Block: {self.player.block}, Energy: {self.player.energy}")
        
        for i, enemy in enumerate(self.enemies):
            if not enemy.is_dead():
                print(f"{i+1}. {enemy.name}: HP {enemy.enemy.current_hp}/{enemy.enemy.max_hp}")

    def player_turn(self):
        """玩家回合"""
        self.player.start_turn()
        print(f"\n--- {self.player.name} 的回合 ---")
        
        while True:
            self.display_state()
            print("\n你的手牌:")
            for i, card in enumerate(self.player.hand):
                print(f"{i}. {card}")
            
            print("\n选择行动:")
            print("p <index> - 打出手牌 (例如: p 0)")
            print("end - 结束回合")
            
            try:
                action = input("请输入指令: ").strip().split()
                if not action:
                    continue
                
                if action[0] == "p" and len(action) > 1:
                    card_index = int(action[1])
                    # 获取存活的敌人作为目标
                    alive_enemies = [enemy for enemy in self.enemies if not enemy.is_dead()]
                    if alive_enemies:
                        self.player.play_card(card_index, [alive_enemies[0]])  # 默认攻击第一个敌人
                    else:
                        print("没有可攻击的敌人!")
                
                elif action[0] == "end":
                    break
                    
            except (ValueError, IndexError):
                print("无效输入，请重新输入!")

        self.player.end_turn()

    def enemy_turn(self):
        """敌人回合"""
        print(f"\n--- 敌人回合 ---")
        for enemy in self.enemies:
            if not enemy.is_dead():
                enemy.take_turn(self.player)

    def start_battle(self):
        """开始战斗"""
        print("=== 战斗开始 ===")
        
        # 初始化玩家卡组
        self.player.draw_pile = self.player.deck.copy()
        random.shuffle(self.player.draw_pile)
        
        turn_count = 1
        while True:
            # 检查战斗是否结束
            over, result = self.is_battle_over()
            if over:
                if result == "win":
                    print("\n🎉 战斗胜利! 🎉")
                else:
                    print("\n💀 战斗失败... 💀")
                break
            
            print(f"\n{'='*20} 第 {turn_count} 回合 {'='*20}")
            
            # 玩家回合
            self.player_turn()
            
            # 再次检查战斗是否结束（可能在最后一击时获胜）
            over, result = self.is_battle_over()
            if over:
                if result == "win":
                    print("\n🎉 战斗胜利! 🎉")
                else:
                    print("\n💀 战斗失败... 💀")
                break
            
            # 敌人回合
            self.enemy_turn()
            
            turn_count += 1


# 示例游戏初始化
def create_sample_deck() -> List[Card]:
    """创建示例卡组"""
    deck = [
        AttackCard("重击", 2, 14),
        AttackCard("痛击", 1, 8),
        AttackCard("连续拳", 1, 5),
        SkillCard("防御", 1, block=5),
        SkillCard("闪避", 1, block=8),
        SkillCard("治疗", 1, heal=6),
        AttackCard("猛击", 2, 16),
        SkillCard("坚固", 1, block=12),
    ]
    return deck


if __name__ == "__main__":
    # 创建玩家
    player = Player("英雄", 80)
    player.deck = create_sample_deck()
    
    # 创建敌人
    enemies = [Enemy("哥布林", 40)]
    
    # 开始战斗
    battle = Battle(player, enemies)
    battle.start_battle()