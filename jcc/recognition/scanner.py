"""游戏状态扫描器 — 整合截图 + 区域裁剪 + OCR"""

import time

import numpy as np

from jcc.adb import ADBController
from jcc.recognition import screen_zones as zones
from jcc.recognition.game_state import GameState, PlayerState
from jcc.recognition.ocr import recognize_number, recognize_text, crop_zone


class GameScanner:
    """扫描游戏画面，输出结构化的 GameState"""

    def __init__(self, adb: ADBController):
        self.adb = adb

    def scan_my_state(self, img: np.ndarray) -> PlayerState:
        """从当前画面识别自己的状态"""
        state = PlayerState()
        state.gold = recognize_number(img, zones.GOLD) or 0
        state.level = recognize_number(img, zones.LEVEL) or 1
        state.hp = recognize_number(img, zones.HP) or 100
        return state

    def scan_shop(self, img: np.ndarray) -> list[str]:
        """识别商店 5 个棋子名称"""
        names = []
        for slot in zones.SHOP_SLOTS:
            name = recognize_text(img, slot)
            names.append(name if name else "")
        return names

    def scan_stage(self, img: np.ndarray) -> str:
        """识别当前阶段 如 '3-2'"""
        return recognize_text(img, zones.STAGE)

    def scan_opponent(self, index: int) -> PlayerState:
        """切换到对手视角，扫描对手状态

        Args:
            index: 对手编号 0-6
        """
        # 点击对手头像切换视角
        portrait = zones.OPPONENT_PORTRAITS[index]
        cx = portrait[0] + portrait[2] // 2
        cy = portrait[1] + portrait[3] // 2
        self.adb.tap(cx, cy)
        time.sleep(0.5)  # 等待画面切换

        img = self.adb.screenshot()
        state = PlayerState()
        state.hp = recognize_number(img, zones.SCOUT_HP) or 0
        state.level = recognize_number(img, zones.SCOUT_LEVEL) or 0
        # 对手金币在侦查视角下可能不可见，尝试识别
        state.gold = recognize_number(img, zones.GOLD) or 0
        return state

    def scan_all(self, scout_opponents: bool = False) -> GameState:
        """扫描完整游戏状态

        Args:
            scout_opponents: 是否侦查所有对手（会依次点击头像，耗时较长）
        """
        img = self.adb.screenshot()

        game = GameState()
        game.me = self.scan_my_state(img)
        game.shop = self.scan_shop(img)
        game.stage = self.scan_stage(img)

        if scout_opponents:
            for i in range(7):
                game.opponents[i] = self.scan_opponent(i)
            # 切回自己的视角（点击自己的头像或棋盘区域）
            self.adb.tap(640, 400)
            time.sleep(0.3)

        return game
