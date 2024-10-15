import heapq
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Node:
    def __init__(self, position, parent=None):
        self.position = position  # (x, y)
        self.parent = parent
        self.g = 0  # 到目前節點的移動成本
        self.h = 0  # 預估的剩餘距離（啟發函數）
        self.f = 0  # f = g + h

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    """使用歐氏距離作為啟發函數"""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def is_valid_move(grid, current_pos, neighbor_pos):
    """檢查移動是否合法（避免穿越牆角）"""
    cx, cy = current_pos
    nx, ny = neighbor_pos

    # 檢查是否在地圖範圍內
    if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
        return False

    # 檢查是否為障礙物
    if grid[nx][ny] == 1:
        return False

    # 若為斜向移動，需檢查水平和垂直方向是否可通行
    if abs(cx - nx) == 1 and abs(cy - ny) == 1:
        if grid[cx][ny] == 1 or grid[nx][cy] == 1:
            return False

    return True

def a_star_search(grid, start, goal):
    """A* 搜尋演算法"""
    open_list = []
    closed_list = set()

    start_node = Node(start)
    goal_node = Node(goal)

    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node == goal_node:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # 反轉路徑

        closed_list.add(current_node.position)

        # 8方向移動
        neighbors = [
            (0, 1), (1, 0), (0, -1), (-1, 0),  # 上下左右
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # 斜向移動
        ]
        for offset in neighbors:
            neighbor_pos = (current_node.position[0] + offset[0],
                            current_node.position[1] + offset[1])

            if is_valid_move(grid, current_node.position, neighbor_pos):
                neighbor_node = Node(neighbor_pos, current_node)

                if neighbor_node.position in closed_list:
                    continue

                neighbor_node.g = current_node.g + heuristic(current_node.position, neighbor_node.position)
                neighbor_node.h = heuristic(neighbor_node.position, goal_node.position)
                neighbor_node.f = neighbor_node.g + neighbor_node.h

                if any(open_node for open_node in open_list if neighbor_node == open_node and neighbor_node.g > open_node.g):
                    continue

                heapq.heappush(open_list, neighbor_node)

    return None  # 無法找到路徑

def animate_path(grid, path):
    """使用 Matplotlib 顯示路徑動畫"""
    fig, ax = plt.subplots()
    ax.imshow(grid, cmap='gray')

    # 初始化船隻位置和路徑線
    point, = ax.plot([], [], 'ro', markersize=8)
    line, = ax.plot([], [], 'r-', linewidth=2)

    # 設定圖表範圍
    ax.set_xlim(-0.5, len(grid[0]) - 0.5)
    ax.set_ylim(len(grid) - 0.5, -0.5)  # y軸方向需反轉，與網格對齊

    def update(frame):
        # 更新船隻位置和經過的路線
        x, y = path[frame]
        point.set_data([y], [x])

        # 畫出經過的路徑
        if frame > 0:
            xdata, ydata = zip(*[(p[1], p[0]) for p in path[:frame + 1]])
            line.set_data(xdata, ydata)

        return point, line

    ani = animation.FuncAnimation(fig, update, frames=len(path), interval=500, repeat=False)
    plt.show()

# 測試範例
if __name__ == "__main__":
    grid = [
        [0, 0, 0, 0, 1],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    start = (0, 0)
    goal = (4, 4)

    path = a_star_search(grid, start, goal)

    if path:
        print("找到的路徑:", path)
        animate_path(grid, path)
    else:
        print("無法找到路徑")
