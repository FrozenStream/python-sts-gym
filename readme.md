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
├── Cards.py          # 卡牌类定义
├── CombatContext.py  # 战斗上下文和核心逻辑
├── CommandIO.py      # 命令行输入输出处理
├── Enemys.py         # 敌人类定义
├── Entity.py         # 实体基类（玩家和敌人的父类）
├── Instances.py      # 具体实例（特定卡牌和敌人）
├── Player.py         # 玩家类定义
├── Powers.py         # 状态效果系统
├── STS_Gym.py        # 强化学习环境接口
├── human_main.py     # 人类玩家入口
└── rl_main.py        # 强化学习训练入口
```

## 核心组件

### Entity 实体系统
- [Entity.py](file:///d:/tmp/Slay-the-Spire-in-Python/Entity.py) 定义了所有战斗单位的基础属性和方法，如生命值、护盾、状态效果等
- [Player.py](file:///d:/tmp/Slay-the-Spire-in-Python/Player.py) 继承自Entity，代表玩家角色
- [Enemys.py](file:///d:/tmp/Slay-the-Spire-in-Python/Enemys.py) 定义了敌人基类及行为模式

### Cards 卡牌系统
- [Cards.py](file:///d:/tmp/Slay-the-Spire-in-Python/Cards.py) 定义了卡牌基类
- [Instances.py](file:///d:/tmp/Slay-the-Spire-in-Python/Instances.py) 包含具体卡牌实例，如攻击卡、防御卡等

### Combat 战斗系统
- [CombatContext.py](file:///d:/tmp/Slay-the-Spire-in-Python/CombatContext.py) 是整个战斗系统的核心，管理战斗流程、回合控制、动作队列等
- [Powers.py](file:///d:/tmp/Slay-the-Spire-in-Python/Powers.py) 实现了各种状态效果（力量、虚弱、荆棘等）

### Interfaces 接口
- [human_main.py](file:///d:/tmp/Slay-the-Spire-in-Python/human_main.py) 提供人类玩家可以直接交互的游戏入口
- [rl_main.py](file:///d:/tmp/Slay-the-Spire-in-Python/rl_main.py) 和 [STS_Gym.py](file:///d:/tmp/Slay-the-Spire-in-Python/STS_Gym.py) 提供强化学习训练环境

## 运行方式

### 人类玩家模式
```bash
python human_main.py
```
运行后可通过命令行进行游戏操作，根据提示选择卡牌或目标。

### 强化学习模式
```bash
python rl_main.py
```
该模式为强化学习算法提供了标准的Gym接口，可用于训练AI玩家。

## 当前实现内容

### 已实现功能
- 基础战斗系统
- 攻击和防御卡牌
- Jaw Worm敌人（两种行动模式）
- 状态效果系统
- 能量管理系统
- 抽牌和弃牌堆机制

### 示例内容
- 玩家拥有80点生命值
- 初始卡组包含4张攻击卡和4张防御卡
- 对战一个Jaw Worm敌人（10点生命值）

## 扩展性设计

本项目采用模块化设计，易于扩展：

1. 添加新卡牌：在[Instances.py](file:///d:/tmp/Slay-the-Spire-in-Python/Instances.py)中定义新的卡牌实例
2. 添加新敌人：在[Enemys.py](file:///d:/tmp/Slay-the-Spire-in-Python/Enemys.py)基础上扩展，并在[Instances.py](file:///d:/tmp/Slay-the-Spire-in-Python/Instances.py)中实现具体敌人
3. 添加新状态效果：在[Powers.py](file:///d:/tmp/Slay-the-Spire-in-Python/Powers.py)中添加新的状态枚举和相关逻辑
4. 训练AI模型：完善[STS_Gym.py](file:///d:/tmp/Slay-the-Spire-in-Python/STS_Gym.py)中的接口以适配不同的强化学习算法

## 开发计划

未来可能的改进方向：
- 更多类型的卡牌和敌人
- 更丰富的状态效果系统
- 完善强化学习接口
- 图形用户界面
- 更复杂的游戏机制（遗物、能力等）

## 使用说明

此项目主要用于学习和研究目的，展示了如何用Python构建一个复杂的卡牌游戏系统，并为强化学习提供训练环境。