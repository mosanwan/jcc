# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

JCC - AI 玩金铲铲之战（Teamfight Tactics）。通过 ADB 连接 Windows 上的安卓模拟器，截图识别游戏状态，AI 决策后自动操作。

## 运行

```bash
pip install -r requirements.txt
python main.py  # 需要先启动安卓模拟器
```

## 架构

核心流水线：`截图 → 识别游戏状态 → AI决策 → 执行操作 → 循环`

三层分离：
- **`jcc/adb/`** — 底层控制：通过 ADB 与模拟器交互（截图、点击、拖拽）。`ADBController` 是唯一入口，所有模拟器操作都经过它
- **`jcc/recognition/`** — 游戏状态识别：CV/OCR 解析截图，输出结构化的游戏状态（金币、血量、商店、棋盘等）
- **`jcc/strategy/`** — AI 决策：根据游戏状态决定操作（买卖棋子、升级、站位等）

`config.py` 是全局配置（ADB 地址端口、游戏分辨率），所有模块都从这里读配置。

## 关键约定

- 游戏目标分辨率 1280x720，所有坐标基于此分辨率
- 截图返回 OpenCV BGR 格式的 numpy 数组
- ADB 命令通过 subprocess 调用，不使用 adb python 库
- 代码注释用中文
- 模拟器为腾讯手游助手（GameLoop），ADB 默认端口 5555
