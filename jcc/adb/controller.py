"""ADB 控制器：连接模拟器、截图、点击、拖拽"""

import subprocess
import time
from pathlib import Path

import cv2
import numpy as np

import config


class ADBController:
    """通过 ADB 控制安卓模拟器"""

    def __init__(self, host: str = None, port: int = None):
        self.host = host or config.ADB_HOST
        self.port = port or config.ADB_PORT
        self.device = f"{self.host}:{self.port}"

    def _run(self, args: list[str], raw: bool = False) -> bytes | str:
        """执行 ADB 命令"""
        cmd = ["adb", "-s", self.device] + args
        result = subprocess.run(cmd, capture_output=True, timeout=10)
        if result.returncode != 0:
            err = result.stderr.decode(errors="ignore").strip()
            raise RuntimeError(f"ADB 命令失败: {' '.join(cmd)}\n{err}")
        return result.stdout if raw else result.stdout.decode(errors="ignore").strip()

    def connect(self) -> bool:
        """连接到模拟器"""
        result = subprocess.run(
            ["adb", "connect", self.device],
            capture_output=True, text=True, timeout=10,
        )
        output = result.stdout.strip()
        print(f"[ADB] {output}")
        return "connected" in output.lower()

    def is_connected(self) -> bool:
        """检查设备是否已连接"""
        result = subprocess.run(
            ["adb", "devices"], capture_output=True, text=True, timeout=5,
        )
        return self.device in result.stdout

    def screenshot(self) -> np.ndarray:
        """截图并返回 OpenCV 格式的图像 (BGR)"""
        png_data = self._run(["exec-out", "screencap", "-p"], raw=True)
        arr = np.frombuffer(png_data, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            raise RuntimeError("截图解码失败")
        return img

    def save_screenshot(self, path: str = None) -> str:
        """截图并保存到文件"""
        img = self.screenshot()
        if path is None:
            Path(config.SCREENSHOT_DIR).mkdir(exist_ok=True)
            path = f"{config.SCREENSHOT_DIR}/{int(time.time())}.png"
        cv2.imwrite(path, img)
        print(f"[ADB] 截图已保存: {path}")
        return path

    def tap(self, x: int, y: int):
        """点击指定坐标"""
        self._run(["shell", "input", "tap", str(x), str(y)])

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300):
        """从 (x1,y1) 滑动到 (x2,y2)，用于拖拽棋子"""
        self._run([
            "shell", "input", "swipe",
            str(x1), str(y1), str(x2), str(y2), str(duration_ms),
        ])

    def long_press(self, x: int, y: int, duration_ms: int = 800):
        """长按指定坐标"""
        self.swipe(x, y, x, y, duration_ms)

    def get_resolution(self) -> tuple[int, int]:
        """获取屏幕分辨率"""
        output = self._run(["shell", "wm", "size"])
        # "Physical size: 1280x720"
        size_str = output.split(":")[-1].strip()
        w, h = size_str.split("x")
        return int(w), int(h)
