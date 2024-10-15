import random

from model.Cell import Cell


import matplotlib.pyplot as plt
import numpy as np

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

def update_map_at(map, cell, TL):
    len_x = len(map)
    len_y = len(map[0])
    for i in range(8):
        x = cell.x + directions[i][0]
        y = cell.y + directions[i][1]
        if 0 <= x < len_x and 0 <= y < len_y:
            neighbor = map[x][y]
            if neighbor.block == 0 and neighbor.vis == 0:
                new_AT = cell.AT + directions[i][2]
                if neighbor.AT > new_AT:
                    neighbor.AT = new_AT
                    TL.append(neighbor)

def plot_path(map, path):
    map_array = np.array([[cell.AT for cell in row] for row in map])
    plt.imshow(map_array, cmap='hot', interpolation='nearest')

    path_x = [cell.x for cell in path]
    path_y = [cell.y for cell in path]

    plt.plot(path_y, path_x, marker='o', color='cyan')
    plt.colorbar()
    plt.show()


def plot_AT_map_with_values(map):
    AT_array = np.array([[cell.AT for cell in row] for row in map])
    plt.imshow(AT_array, cmap='hot', interpolation='nearest')
    plt.colorbar()

    for i in range(len(map)):
        for j in range(len(map[0])):
            plt.text(j, i, f'{map[i][j].AT:.1f}', ha='center', va='center', color='black')

    plt.show()

def plot_AT_map_with_obstacles(map):
    AT_array = np.array([[cell.AT for cell in row] for row in map])
    plt.imshow(AT_array, cmap='hot', interpolation='nearest')
    plt.colorbar()

    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j].block == 1:
                plt.gca().add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=True, color='blue', alpha=0.5))

    plt.show()

def at_array_covered(map):
    AT_list = []
    for i in range(len(map)):
        AT_list.append([])
        for j in range(len(map[0])):
            AT_list[i].append(map[i][j].AT)

    return np.array(AT_list)

def plot_map_with_obstacles_and_path(map, path):
    AT_array = at_array_covered(map)
    plt.imshow(AT_array, cmap='hot', interpolation='nearest', alpha=0.3, origin='lower')
    plt.colorbar()

    for i in range(len(map)):
        for j in range(len(map[0])):
            #plt.text(j, i, f'{map[i][j].AT:.1f}', ha='center', va='center', color='black')
            if map[i][j].block == 1:
                plt.gca().add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=True, color='blue', alpha=0.5))

    path_x = [cell.x for cell in path]
    path_y = [cell.y for cell in path]
    plt.plot(path_y, path_x, marker='o', color='cyan')

    plt.show()

def plot_map_with_obstacles_and_path_no_at(map, path):
    AT_array = at_array_covered(map)
    plt.imshow(AT_array, cmap='hot', interpolation='nearest', alpha=0.3, origin='lower')
    plt.colorbar()
    path_x = [cell.x for cell in path]
    path_y = [cell.y for cell in path]
    plt.plot(path_y, path_x, marker='o', color='cyan')

    plt.show()
def create_map(x, y):
    return [[Cell(i, j) for j in range(y)] for i in range(x)]

def add_random_obstacles(map, obstacle_count):
    len_x = len(map)
    len_y = len(map[0])
    for _ in range(obstacle_count):
        x = random.randint(0, len_x - 1)
        y = random.randint(0, len_y - 1)
        map[x][y].block = 1



if __name__ == '__main__':
    #計時
    import time
    start = time.time()

    # 新增地圖空間
    map = create_map(100, 100)

    # 設定起點與終點
    start_position = map[0][0]
    end_position = map[99][99]

    # 設定起點的 AT 為 0
    start_position.AT = 0

    # 顯示地圖 幫我對齊
    #plot_AT_map_with_obstacles(map)





    #陣列初始化
    tl, ll0, ll1, ll2 = [], [], [], []
    ll0_head, ll1_head, ll2_head = 0, 1, 2
    index = 0

    #將起點加入 TL
    tl.append(start_position)
    start_position.vis = 1

    #將 TL 中的 cell 分配到 LL0, LL1, LL2
    while end_position.vis != 1 :
        # print("----------------------------------------------------------------")
        # for i in range(len(map)):
        #     for j in range(len(map[0])):
        #         print(f'{map[i][j].AT:.2f}', end=' ')
        #     print()
        if len(tl) == 0:
            plot_AT_map_with_values(map)
            print("No path found")
            break
        while tl:
            cell = tl.pop()
            if ll0_head <= cell.AT < ll0_head + 1:
                ll0.append(cell)
            elif ll1_head <= cell.AT < ll1_head + 1:
                ll1.append(cell)
            elif ll2_head <= cell.AT < ll2_head + 1:
                ll2.append(cell)

        #根據index 更新 LL0, LL1, LL2
        if index == 0:
            for cell in ll0:
                cell.vis = 1
                update_map_at(map, cell, tl)
            ll0_head += 3
            index = 1

        elif index == 1:
            for cell in ll1:
                cell.vis = 1
                update_map_at(map, cell, tl)
            ll1_head += 3
            index = 2

        elif index == 2:
            for cell in ll2:
                cell.vis = 1
                update_map_at(map, cell, tl)
            ll2_head += 3
            index = 0

    #顯示地圖
    #plot_AT_map_with_values(map)

    #回朔路線
    path = []
    cell = end_position

    while cell != start_position:
        path.append(cell)
        min_AT = float('inf')
        next_cell = None
        for i in range(8):
            x = cell.x + directions[i][0]
            y = cell.y + directions[i][1]
            if 0 <= x < len(map) and 0 <= y < len(map[0]):
                neighbor = map[x][y]
                if neighbor.AT < min_AT:
                    min_AT = neighbor.AT
                    next_cell = neighbor
        cell = next_cell

    path.append(start_position)
    path.reverse()

    # for i in range(len(map)):
    #     for j in range(len(map[0])):
    #         print(f'{map[i][j].AT:.2f}', end=' ')
    #     print()

    print("Time:", time.time()-start)



    # 使用 matplotlib 顯示路線
    plot_map_with_obstacles_and_path(map, path)


