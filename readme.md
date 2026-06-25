# 🎬 Bad Apple ASCII 特殊符号转换动画 (Python)

一个使用 **Python** 编写的 ASCII 视频播放器，可将任何 MP4 视频实时转换为 ASCII 特殊符号动画，并同步播放原始音频。

整个项目代码采用 **西班牙语** 编写。

---

# ✨ 功能特点

- 🎥 将 MP4 视频转换为 ASCII 特殊符号动画
- 🎵 自动提取视频音频并同步播放
- 🖥️ Terminal（CMD）播放模式
- 🪟 Tkinter 全屏窗口播放模式
- 📊 实时转换进度条
- ⚡ 30 FPS 流畅播放
- 📐 自动保持视频比例
- 🔍 动态窗口字体缩放
- 📺 支持全屏 ASCII 视频显示
- 🎬 支持任何 MP4 视频

---

# 📦 Python 依赖库

安装 Python 后，执行：

```bash
pip install opencv-python
pip install pillow
pip install pygame
pip install fpstimer
pip install moviepy
```

或者一次安装：

```bash
pip install opencv-python pillow pygame fpstimer moviepy
```

---

# 📚 使用到的 Python 模块

```python
import cv2
import time
import sys
from PIL import Image
import os
import tkinter as tk

# Desactivar el prompt de pygame antes de importarlo
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import fpstimer
import moviepy.editor as mp
```

---

# ▶ 使用方法

运行：

```bash
python main.py
```

程序启动后会显示菜单：

```text
==============================================================

Seleccione una opción:

1) Reproducir Video
2) Auto - video existente con el nombre video.mp4
3) Ejecutar en la Ventana
4) Salir

==============================================================
```

## 1️⃣ Reproducir Video

输入视频名称（无需 `.mp4`），程序会：

- 提取视频音频
- 将所有视频帧转换为 ASCII
- 在 CMD 中同步播放动画与音频

---

## 2️⃣ Auto

自动读取：

```text
video.mp4
```

无需输入文件名。

---

## 3️⃣ Ejecutar en la Ventana

使用 Tkinter 全屏窗口播放 ASCII 视频。

支持：

- 全屏显示
- 自动字体缩放
- 自动放大 ASCII 图像
- 同步播放音频
- 更好的观看体验

---

# ⚙ 工作流程

```text
MP4 Video
     │
     ▼
 OpenCV 读取视频
     │
     ▼
 RGB 转换
     │
     ▼
 Pillow 灰度处理
     │
     ▼
 ASCII 字符映射
     │
     ▼
 缓存所有 ASCII 帧
     │
     ├──────────────► MoviePy 提取音频
     │                         │
     ▼                         ▼
CMD / Tkinter              pygame 播放音频
     │                         │
     └────────── 同步播放 ──────────┘
```

---

# 🛠 使用到的技术

- Python
- OpenCV
- Pillow (PIL)
- Tkinter
- pygame
- MoviePy
- FPSTimer

---

# 📂 支持格式

视频：

```text
MP4
```

音频：

程序会自动提取：

```text
audio.mp3
```

---

# 🚀 项目特点

相比普通 ASCII 播放器，本项目具有：

- 更稳定的视频播放
- 自动提取视频音频
- 音画同步播放
- Terminal 与 Tkinter 双播放模式
- 自动保持视频比例
- 动态字体缩放
- 实时转换进度显示
- 支持全屏 ASCII 视频播放
- 流畅的 30 FPS 播放体验

---

# 📄 License

This project is open source.