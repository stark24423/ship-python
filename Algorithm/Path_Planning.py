import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
import model.Cell as Cell
import model.list_magerment as List_Manager













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

def create_map(x, y):
    return [[Cell.Cell(i, j) for j in range(y)] for i in range(x)]

def convert_map_to_array(map):
    return np.array([[cell.AT for cell in row] for row in map])

def plot_map(map):
    map_array = convert_map_to_array(map)
    plt.imshow(map_array, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.show()

def update_map_at(map, cell, TL):
    for i in range(8):
        x = cell.x + directions[i][0]
        y = cell.y + directions[i][1]
        if 0 <= x < len(map) and 0 <= y < len(map[0]):
            neighbor = map[x][y]
            if neighbor.block == 0 and neighbor.vis == 0:
                new_AT = cell.AT + directions[i][2]
                if neighbor.AT > new_AT:
                    neighbor.AT = new_AT
                    TL_push(TL, neighbor)

def assign_TL_to_LL(TL, LL0, LL1, LL2, index):

    while TL:
        cell = TL.pop()
        if index<=cell.AT<=index+1:
            index+=1

        if index%3 == 0:
            LL0.append(cell)
        if index%3 == 1:
            LL1.append(cell)
        if index%3 == 2:
            LL2.append(cell)

def process_LL(LL, TL, map):
    while LL:
        cell = LL.pop()
        update_map_at(map, cell, TL)
        cell.vis = 1

#show map block
def show_map_block(map):
    for i in range(len(map)):
        for j in range(len(map[0])):
            print(map[i][j].block, end=' ')
        print()

#show map AT
def show_map_AT(map):
    for i in range(len(map)):
        for j in range(len(map[0])):
            print(map[i][j].AT, end=' ')
        print()

def TL_push(TL, cell):
    cell.vis = 1
    TL.append(cell)


def path_planning(start_position, end_position, map):
    lm = List_Manager.List_Manager()
    start_position.AT = 0
    lm.TL_push(start_position)
    index = 0

    while end_position.vis != 1:


        lm.assign_TL_to_LL()


        if index%3  == 0:
            process_LL(lm.LL0, lm.TL, map)
            lm.LL0_head += 3
        elif index%3 == 1:
            process_LL(lm.LL1, lm.TL, map)
            lm.LL1_head += 3
        elif index%3 == 2:
            process_LL(lm.LL2, lm.TL, map)
            lm.LL2_head += 3
        index += 1
        plot_map(map)


if __name__ == '__main__':
    map = create_map(8, 8)
    start_position = map[0][0]
    end_position = map[7][7]




    path_planning(start_position, end_position, map)
    show_map_AT(map)
    plot_map(map)
