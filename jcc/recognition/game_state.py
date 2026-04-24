"""游戏状态数据模型"""

from dataclasses import dataclass, field


@dataclass
class Champion:
    """棋子"""
    name: str = ""
    star: int = 1           # 星级 1/2/3
    position: tuple = ()    # 棋盘坐标 (row, col)
    items: list[str] = field(default_factory=list)


@dataclass
class PlayerState:
    """玩家状态（自己或对手）"""
    hp: int = 100
    level: int = 1
    gold: int = 0
    board: list[Champion] = field(default_factory=list)   # 场上棋子
    bench: list[Champion] = field(default_factory=list)    # 备战席（仅自己）


@dataclass
class GameState:
    """完整游戏状态"""
    me: PlayerState = field(default_factory=PlayerState)
    opponents: dict[int, PlayerState] = field(default_factory=dict)  # 对手编号 → 状态
    shop: list[str] = field(default_factory=list)          # 商店 5 个棋子
    stage: str = ""                                         # 当前阶段 如 "3-2"
    round_timer: int = 0                                    # 回合剩余时间（秒）
