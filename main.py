"""JCC - AI 玩金铲铲之战"""

from jcc.adb import ADBController


def main():
    adb = ADBController()

    # 1. 连接模拟器
    if not adb.connect():
        print("连接模拟器失败，请检查模拟器是否启动")
        return

    # 2. 检查分辨率
    w, h = adb.get_resolution()
    print(f"[INFO] 模拟器分辨率: {w}x{h}")

    # 3. 测试截图
    path = adb.save_screenshot()
    print(f"[INFO] 截图测试成功: {path}")

    # 4. 测试点击（屏幕中心）
    cx, cy = w // 2, h // 2
    print(f"[INFO] 测试点击屏幕中心: ({cx}, {cy})")
    adb.tap(cx, cy)

    print("\n✓ ADB 模块测试通过，基础功能正常")


if __name__ == "__main__":
    main()
