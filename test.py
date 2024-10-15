import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 建立船隻的移動路徑 (100 個點的 x 和 y)
path_x = np.linspace(0, 10, 100)
path_y = np.sin(path_x)  # y 為 sin 波

fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)

# 添加網格
ax.grid(True)  # 打開網格

# 用藍色圓點代表船隻
ship, = ax.plot([], [], 'bo', markersize=10)

def update(frame):
    # 更新船隻的位置
    ship.set_data([path_x[frame]], [path_y[frame]])
    return ship,

# 創建動畫
ani = FuncAnimation(fig, update, frames=len(path_x), interval=100, blit=True)

# 顯示圖表
plt.show()
