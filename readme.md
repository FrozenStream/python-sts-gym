# Slay the Spire in Python

这是一个使用Python实现的类似《杀戮尖塔(Slay the Spire)》的卡牌游戏原型。该项目旨在提供一个可扩展的游戏框架，支持人类玩家操作以及强化学习训练环境。

## 项目概述

本项目实现了《杀戮尖塔》的核心战斗机制，包括：
- 玩家与敌人的回合制战斗
- 卡牌系统（攻击、防御等基础卡牌）
- 状态效果系统（力量、敏捷、荆棘等）
- 回合能量管理
- 抽牌、弃牌堆机制

## 文件结构

```
.
├── Cards.py             # 卡牌类定义
├── CombatContext.py     # 战斗上下文和核心逻辑
├── CommandIO.py         # 命令行输入输出处理
├── Entity.py            # 实体基类（玩家和敌人的父类）
├── InstancesCard.py     # 具体卡牌实例
├── InstancesEnemy.py    # 具体敌人实例
├── Powers.py            # 状态效果系统
├── STS_Gym.py           # 强化学习环境接口
└── main.py              # 游戏主入口
```

## 自定义内容指南

### 添加新卡牌

要在游戏中添加新卡牌，需要执行以下步骤：

1. 在 [InstancesCard.py](file:///d:/tmp/Slay-the-Spire-in-Python/InstancesCard.py) 的 [CardLambdas](file:///d:/tmp/Slay-the-Spire-in-Python/InstancesCard.py#L7-L22) 字典中定义卡牌效果：
   ```python
   CardLambdas: Dict[str, Tuple[Callable[[CombatContext], None], ...]] = {
       // ...现有卡牌...
       
       // 新增卡牌示例
       'new_card': (
           lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
           lambda context: attackEntity(context, context.player, context.getChoice(), 10),
       ),
   }
   ```

2. 在同一文件中创建卡牌实例：
   ```python
   new_card = Card('new_card', 1, CardType.ATTACK, CardLambdas['new_card'])
   ```

3. 将新卡牌添加到 [main.py](file:///d:/tmp/Slay-the-Spire-in-Python/main.py) 中的卡组列表：
   ```python
   cards = [
       // ...现有卡牌...
       new_card,  // 添加新卡牌
   ]
   ```

### 添加新敌人

要添加新的敌人类型，请按以下步骤操作：

1. 在 [InstancesEnemy.py](file:///d:/tmp/Slay-the-Spire-in-Python/InstancesEnemy.py) 中创建一个新的敌人类：
   ```python
   class NewEnemy(Enemy):
       def __init__(self, max_hp: int = 20):
           super().__init__('New Enemy', max_hp)
       
       def move(self, context: CombatContext, turns: int):
           if self.OUT: return
           // 实现敌人的行为逻辑
           attackEntity(context, self, context.player, 5)
   ```

2. 在 [main.py](file:///d:/tmp/Slay-the-Spire-in-Python/main.py) 中添加敌人实例：
   ```python
   enemy = [
       // ...现有敌人...
       NewEnemy(),  // 添加新敌人
   ]
   ```

### 添加新状态效果

要添加新的状态效果，请按以下步骤操作：

1. 在 [Powers.py](file:///d:/tmp/Slay-the-Spire-in-Python/Powers.py) 的 [Power](file:///d:/tmp/Slay-the-Spire-in-Python/Powers.py#L4-L12) 枚举中添加新的状态：
   ```python
   class Power(Enum):
       // ...现有状态...
       NEW_STATE = 7  // 新状态
   ```

2. 在 [CombatContext.py](file:///d:/tmp/Slay-the-Spire-in-Python/CombatContext.py) 中的相关函数里处理新状态的效果：
   ```python
   def someFunction(context: CombatContext, target: Entity, ...):
       // 处理新状态效果
       if target.power_pool.getPower(Power.NEW_STATE) > 0:
           // 实现状态效果逻辑
   ```

### 修改现有内容

#### 修改玩家初始属性
在 [main.py](file:///d:/tmp/Slay-the-Spire-in-Python/main.py) 中修改玩家初始化参数：
```python
player = Player('Player', 100)  // 修改初始生命值为100
```

#### 修改敌人属性
在 [main.py](file:///d:/tmp/Slay-the-Spire-in-Python/main.py) 中修改敌人初始化参数：
```python
enemy = [
    JawWorm(15),  // 修改Jaw Worm的生命值为15
]
```

## 运行游戏

### 人类玩家模式
```bash
python main.py
```
运行后可通过命令行进行游戏操作，根据提示选择卡牌或目标。

## 核心组件详解

### Entity 实体系统
- [Entity.py](file:///d:/tmp/Slay-the-Spire-in-Python/Entity.py) 定义了所有战斗单位的基础属性和方法，如生命值、护盾、状态效果等
- [Player](file:///d:/tmp/Slay-the-Spire-in-Python/Entity.py#L33-L35) 类继承自 [Entity](file:///d:/tmp/Slay-the-Spire-in-Python/Entity.py#L3-L17)，代表玩家角色
- [Enemy](file:///d:/tmp/Slay-the-Spire-in-Python/Entity.py#L38-L40) 类是敌人基类，可在其基础上扩展更多敌人类型

### Cards 卡牌系统
- [Cards.py](file:///d:/tmp/Slay-the-Spire-in-Python/Cards.py) 定义了卡牌基类
- [InstancesCard.py](file:///d:/tmp/Slay-the-Spire-in-Python/InstancesCard.py) 包含具体卡牌实例，如攻击卡、防御卡等

### Combat 战斗系统
- [CombatContext.py](file:///d:/tmp/Slay-the-Spire-in-Python/CombatContext.py) 是整个战斗系统的核心，管理战斗流程、回合控制、动作队列等
- [Powers.py](file:///d:/tmp/Slay-the-Spire-in-Python/Powers.py) 实现了各种状态效果（力量、虚弱、荆棘等）

## 当前实现内容

### 已实现功能
- 基础战斗系统
- 多种卡牌（攻击、防御、特殊效果）
- Jaw Worm敌人（两种行动模式）
- 状态效果系统
- 能量管理系统
- 抽牌和弃牌堆机制

### 示例内容
- 玩家拥有80点生命值
- 初始卡组包含多种类型的卡牌
- 可对战多个Jaw Worm敌人

## 使用说明

此项目主要用于学习和研究目的，展示了如何用Python构建一个复杂的卡牌游戏系统，并为强化学习提供训练环境。