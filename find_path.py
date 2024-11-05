import heapq
import matplotlib.pyplot as plt


directions = [
    (0, 1, 1),  # 向右
    (1, 0, 1),  # 向下
    (0, -1, 1),  # 向左
    (-1, 0, 1),  # 向上
    (1, 1, 1.4),  # 右下（對角線）
    (1, -1, 1.4),  # 左下（對角線）
    (-1, 1, 1.4),  # 右上（對角線）
    (-1, -1, 1.4)  # 左上（對角線）
]

def cuculate_AT(start , end):
    return math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)

def update_obstacle(max_AT, grid, other_ship_path):
    for ship_path in other_ship_path:
        start = ship_path[0]
        for pos in ship_path:

            if ( max_AT+1 )>cuculate_AT(start,pos) > max_AT:
                grid[pos[0]][pos[1]] = 1
                break
            else:
                grid[pos[0]][pos[1]] = 0



def find_path(start, goal, grid, other_ship_path):
    if start == goal:
        return [start]
    temp = []
    heapq.heappush(temp, (0, start))

    # 建立 AT 表
    AT = [[float('inf')] * len(grid[0]) for _ in range(len(grid))]
    AT[start[0]][start[1]] = 0

    # 建立訪問表
    visited = [[False] * len(grid[0]) for _ in range(len(grid))]
    visited[start[0]][start[1]] = True

    # 建立 came_from 表
    came_from = [[None] * len(grid[0]) for _ in range(len(grid))]
    max_at = 0
    # 迴圈開始
    while temp:

        #step 1 pop temp
        _, current = heapq.heappop(temp)
        if current == goal:
            break
        #step 2 update map
        for i in range(8):
            x = current[0] + directions[i][0]
            y = current[1] + directions[i][1]
            if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                update_obstacle(max_at, grid, other_ship_path)
                if grid[x][y] == 0 and not visited[x][y]:
                    new_AT = AT[current[0]][current[1]] + directions[i][2]
                    if AT[x][y] > new_AT:
                        AT[x][y] = new_AT
                        heapq.heappush(temp, (new_AT, (x, y)))
                        visited[x][y] = True
                        came_from[x][y] = current
    # 回溯路徑
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current[0]][current[1]]
    path.append(start)
    path.reverse()
    print(AT)
    return path, AT





# 測試範例
def main():
    grid = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
    ]
    start = (0, 0)
    goal = (3, 3)

    path, AT = find_path(start, goal, grid)

    if path:
        print("找到路徑：", path)
        # 圖形化顯示
        plt.figure(figsize=(6, 6))
        ax = plt.gca()
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                x, y = j, len(grid) - 1 - i
                if grid[i][j] == 1:
                    plt.plot(x, y, 'ks')  # 障礙物，用黑色方塊表示
                else:
                    # 在可通行的格子上顯示 AT 值
                    if AT[i][j] != float('inf'):
                        plt.text(x, y, int(AT[i][j]), ha='center', va='center', color='blue')
                    else:
                        plt.text(x, y, '∞', ha='center', va='center', color='gray')

        x_coords = [p[1] for p in path]
        y_coords = [len(grid) - 1 - p[0] for p in path]
        plt.plot(x_coords, y_coords, 'ro-')  # 路徑，用紅色線條表示
        plt.plot(start[1], len(grid) - 1 - start[0], 'go')  # 起點，用綠色圓點表示
        plt.plot(goal[1], len(grid) - 1 - goal[0], 'bo')  # 終點，用藍色圓點表示
        plt.title('洪泛路徑規劃結果（包含 AT 值）')
        plt.grid(True)
        plt.xlim(-1, len(grid[0]))
        plt.ylim(-1, len(grid))
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
    else:
        print("未找到路徑")

if __name__ == "__main__":
    main()
