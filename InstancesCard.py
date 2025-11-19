from Cards import Card, CardType
from CombatContext import *
from typing import Callable, Tuple, Dict

CardLambdas: Dict[str, Tuple[Callable[[CombatContext], None], ...]] = {
    'Strike_red': (  # 红色攻击
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackEntity(context, context.player, context.getChoice(), 6, 1),
    ),
    'Defend_red': (  # 红色防御
        lambda context: gainShield(context, context.player, 6),
    ),
    'Dash': (  # 重击
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackEntity(context, context.player, context.getChoice(), 8, 1),
        lambda context: entityGainPower(context, context.getChoice(), Power.VULNERABLE, 2),
    ),
    'Anger': (  # 愤怒
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackEntity(context, context.player, context.getChoice(), 6, 1),
        lambda context: addCardToPile(context, Anger, context.discard_pile),
    ),
    'Head Butt': (  # 头槌
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackEntity(context, context.player, context.getChoice(), 9, 1),
        # TODO / ERROR: This Card does not match the original sts.
    ),
    'Heavy Blade': (  # 重刃
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackEntity(context, context.player, context.getChoice(),
                                     12 + context.player.power_pool.getPower(Power.STRENGTH) * 2, 1),
    ),
    'Iron Wave': (  # 铁斩波
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackEntity(context, context.player, context.getChoice(), 5, 1),
        lambda context: gainShield(context, context.player, 5),
    ),
    'Perfected Strike': (  # 完美打击
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackEntity(context, context.player, context.getChoice(),
                                     6 + countStrike(context), 1),
    ),
    'Pommel Strike': (  # 剑柄打击
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackEntity(context, context.player, context.getChoice(), 9, 1),
        lambda context: drawCards(context, 1),
    ),
    'Sword Boomerang': (  # 飞剑回旋镖
        lambda context: randomAttackEntity(context, context.player, context.enemies, 3, 3),
    ),
    'Thunderclap': (  # 闪电霹雳
        lambda context: attackAllEntity(context, context.player, context.enemies, 4, 1),
        lambda context: allEntityGainPower(context, context.enemies, Power.VULNERABLE, 1),
    ),
    'Twin Strike': (  # 双重打击
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackEntity(context, context.player, context.getChoice(), 5, 2),
    ),
    'Wild Strike': (  # 狂野打击
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackEntity(context, context.player, context.getChoice(), 12, 1),
        # TODO / ERROR: This Card does not match the original sts.
    ),
    'Body Slam': (  # 全身撞击
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackEntity(context, context.player, context.getChoice(), context.player.shield, 1),
    ),
    'Clash': (  # 交锋
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackEntity(context, context.player, context.getChoice(), 14, 1),
    ),
    'Cleave': (  # 顺劈斩
        lambda context: attackAllEntity(context, context.player, context.enemies, 8, 1),
    ),
    'Clothesline': (  # 金刚臂
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackAllEntity(context, context.player, context.getChoice(), 12, 1),
        lambda context: entityGainPower(context, context.getChoice(), Power.WEAK, 2),
    ),
    'Dropkick': (  # 飞身踢
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: ((
            gainEnergy(context, 1),
            drawCards(context, 1),
            attackEntity(context, context.player, context.getChoice(), 5, 1))
            if context.getChoice().power_pool.getPower(Power.VULNERABLE) > 0
            else attackEntity(context, context.player, context.getChoice(), 5, 1)
        )
    ),

    'Bowling Bash': (
        lambda context: context.needChoice(IOtype.CHOOSE_ENTITY),
        lambda context: attackEntity(context, context.player, context.getChoice(),
                                     6 * context.howManyLivingEnemies(), 1),
    ),
    'Prepared': (
        lambda context: drawCards(context, 1),
        lambda context: context.needChoice(IOtype.CHOOSE_DISCARD),
        lambda context: discardCard(context, context.getChoice()),
    ),

}

Strike_red = Card('Strike_red', 1, CardType.ATTACK, CardLambdas['Strike_red'])
Defend_red = Card('Defend_red', 1, CardType.SKILL, CardLambdas['Defend_red'])
Dash = Card('Dash', 2, CardType.ATTACK, CardLambdas['Dash'])
Anger = Card('Anger', 0, CardType.ATTACK, CardLambdas['Anger'])
HeadButt = Card('Head Butt', 1, CardType.ATTACK, CardLambdas['Head Butt'])
HeavyBlade = Card('Heavy Blade', 2, CardType.ATTACK, CardLambdas['Heavy Blade'])
IronWave = Card('Iron Wave', 1, CardType.ATTACK, CardLambdas['Iron Wave'])
PerfectedStrike = Card('Perfected Strike', 1, CardType.ATTACK, CardLambdas['Perfected Strike'])
PommelStrike = Card('Pommel Strike', 1, CardType.ATTACK, CardLambdas['Pommel Strike'])
SwordBoomerang = Card('Sword Boomerang', 1, CardType.ATTACK, CardLambdas['Sword Boomerang'])
Thunderclap = Card('Thunderclap', 1, CardType.ATTACK, CardLambdas['Thunderclap'])
TwinStrike = Card('Twin Strike', 1, CardType.ATTACK, CardLambdas['Twin Strike'])
WildStrike = Card('Wild Strike', 1, CardType.ATTACK, CardLambdas['Wild Strike'])
BodySlam = Card('Body Slam', 1, CardType.ATTACK, CardLambdas['Body Slam'])
Clash = Card('Clash', 1, CardType.ATTACK, CardLambdas['Clash'])
Cleave = Card('Cleave', 1, CardType.ATTACK, CardLambdas['Cleave'])
Clothesline = Card('Clothesline', 2, CardType.ATTACK, CardLambdas['Clothesline'])
Dropkick = Card('Dropkick', 1, CardType.ATTACK, CardLambdas['Dropkick'])


BowlingBash = Card('Bowling Bash', 1, CardType.ATTACK, CardLambdas['Bowling Bash'])
Prepared = Card('Prepared', 1, CardType.SKILL, CardLambdas['Prepared'])
