# JCC - AI 玩金铲铲之战

使用 AI 自动玩金铲铲之战（Teamfight Tactics）的项目。

通过 ADB 连接安卓模拟器，截图识别游戏状态，AI 决策后自动操作。

## 项目结构

```
jcc/
├── config.py              # 配置（ADB地址、分辨率等）
├── main.py                # 入口
├── jcc/
│   ├── adb/               # ADB 控制（截图、点击、拖拽）
│   ├── recognition/       # 游戏状态识别
│   └── strategy/          # AI 决策引擎
└── requirements.txt
```

## 快速开始

```bash
pip install -r requirements.txt
# 启动安卓模拟器，修改 config.py 中的 ADB_PORT
python main.py
```

## 技术栈

- Python + OpenCV（屏幕识别）
- ADB（模拟器控制）
- AI 决策引擎

## 状态

🚧 开发中
