"""JCC - AI 玩金铲铲之战"""

import json
from dataclasses import asdict

from jcc.adb import ADBController
from jcc.recognition import GameScanner


def main():
    adb = ADBController()

    # 1. 连接模拟器
    if not adb.connect():
        print("连接模拟器失败，请检查模拟器是否启动")
        return

    w, h = adb.get_resolution()
    print(f"[INFO] 模拟器分辨率: {w}x{h}")

    # 2. 扫描游戏状态
    scanner = GameScanner(adb)
    state = scanner.scan_all(scout_opponents=False)

    # 3. 输出结构化状态
    print("\n[GameState]")
    print(json.dumps(asdict(state), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
