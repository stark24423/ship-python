import heapq
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import math

# 定義移動方向及其對應的消耗
directions = [
    (0, 1, 1),  # 右
    (1, 0, 1),  # 下
    (0, -1, 1),  # 左
    (-1, 0, 1),  # 上
    (1, 1, 1.4),  # 右下
    (1, -1, 1.4),  # 左下
    (-1, 1, 1.4),  # 右上
    (-1, -1, 1.4)  # 左上
]


def cuculate_AT(start, end):
    return math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)


def set_range_obstale(pos, grid, collision_avoidance_range):
    for i in range(-collision_avoidance_range, collision_avoidance_range):
        for j in range(-collision_avoidance_range, collision_avoidance_range):
            grid[pos[0] + i][pos[1] + j] = 1


def clear_range_obstale(pos, grid, collision_avoidance_range):
    for i in range(-collision_avoidance_range, collision_avoidance_range):
        for j in range(-collision_avoidance_range, collision_avoidance_range):
            grid[pos[0] + i][pos[1] + j] = 0


def update_obstacle(max_AT, dynamic_grid, other_ship_path):
    for ship_path in other_ship_path:
        if ship_path:
            start_pos = ship_path[0]
            for pos in ship_path:
                ship_at = cuculate_AT(start_pos, pos)
                if max_AT< ship_at<max_AT+1:
                    set_range_obstale(pos, dynamic_grid, 1)
                if max_AT-1< ship_at<max_AT:
                    clear_range_obstale(pos, dynamic_grid, 1)



def find_path(start, goal, grid, other_ship_path):
    if start == goal:
        return [start]
    temp = []
    heapq.heappush(temp, (0, start))
    AT = [[float('inf')] * len(grid[0]) for _ in range(len(grid))]
    AT[start[0]][start[1]] = 0
    visited = [[False] * len(grid[0]) for _ in range(len(grid))]
    visited[start[0]][start[1]] = True
    came_from = [[None] * len(grid[0]) for _ in range(len(grid))]
    dynamic_grid = [row[:] for row in grid]
    path_steps = []

    while temp:
        _, current = heapq.heappop(temp)
        if current == goal:
            break
        max_at = AT[current[0]][current[1]]
        update_obstacle(max_at, dynamic_grid, other_ship_path)
        for i in range(8):
            x = current[0] + directions[i][0]
            y = current[1] + directions[i][1]
            if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                if dynamic_grid[x][y] == 0 and not visited[x][y]:
                    new_AT = AT[current[0]][current[1]] + directions[i][2]
                    if AT[x][y] > new_AT:
                        AT[x][y] = new_AT
                        heapq.heappush(temp, (new_AT, (x, y)))
                        visited[x][y] = True
                        came_from[x][y] = current
                        path_steps.append((x, y))

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current[0]][current[1]]
        if current is None:
            return None, AT, path_steps
    path.append(start)
    path.reverse()
    return path, AT, path_steps


# 動畫顯示路徑
def main():
    grid = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]
    start = (0, 0)
    goal = (5, 5)
    other_ship_path = [[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0)]]
    path, AT, path_steps = find_path(start, goal, grid, other_ship_path)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-0.5, len(grid[0]) - 0.5)
    ax.set_ylim(-0.5, len(grid) - 0.5)
    ax.set_xticks(range(len(grid[0])))
    ax.set_yticks(range(len(grid)))
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')
    plt.gca().invert_yaxis()

    # 靜態障礙物繪製
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                ax.plot(j, i, 'ks')  # 障礙物

    # 起點和終點標記
    ax.plot(start[1], start[0], 'go', markersize=10, label='起點')
    ax.plot(goal[1], goal[0], 'bo', markersize=10, label='終點')

    # 添加進度條
    ax_slider = plt.axes([0.2, 0.01, 0.6, 0.03], facecolor="lightgrey")
    slider = Slider(ax_slider, '進度', 0, max(len(path), len(other_ship_path[0])) - 1, valinit=0, valstep=1)

    # 動畫更新函數
    def update(num):
        ax.clear()
        ax.set_xlim(-0.5, len(grid[0]) - 0.5)
        ax.set_ylim(-0.5, len(grid) - 0.5)
        ax.grid(True)
        plt.gca().invert_yaxis()

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    ax.plot(j, i, 'ks')  # 障礙物

        # 當前步驟的動態障礙物
        if num < len(other_ship_path[0]):
            ship_pos = other_ship_path[0][num]
            ax.plot(ship_pos[1], ship_pos[0], 'bx', markersize=8, label='飛機行走路徑')

        # 起點和終點標記
        ax.plot(start[1], start[0], 'go', markersize=10, label='起點')
        ax.plot(goal[1], goal[0], 'bo', markersize=10, label='終點')

        # 繪製路徑規劃的路徑
        for i in range(num + 1):
            if i < len(path):
                step = path[i]
                ax.plot(step[1], step[0], 'ro', markersize=5, label='規劃路徑' if i == 0 else "")

        # 添加圖例
        if num == 0:
            ax.legend(loc="upper right")

    # 初始化動畫
    ani = animation.FuncAnimation(fig, update, frames=max(len(path), len(other_ship_path[0])), interval=500,
                                  repeat=False)

    # 更新動畫隨滑桿
    def on_slider_change(val):
        update(int(slider.val))

    slider.on_changed(on_slider_change)
    plt.show()


if __name__ == "__main__":
    main()
